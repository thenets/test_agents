import time
import re
import ast
import operator
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from .llm_config import configure_llm
from .calculator_tools import get_calculator_tools

def create_calculator_agent():
    """Create a ReAct agent with calculator tools"""
    llm = configure_llm()
    tools = get_calculator_tools()
    
    # Create the ReAct agent with calculator tools and system prompt
    agent = create_react_agent(
        llm, 
        tools,
        prompt="""You are a helpful calculator assistant. When asked to perform mathematical calculations, 
        you should use the provided calculator tools (add, subtract, multiply, divide) to compute the results accurately.
        Always use the tools for calculations rather than doing math in your head."""
    )
    
    return agent

def extract_numerical_result(final_answer):
    """Extract numerical result from the final answer text.
    
    Args:
        final_answer: String containing the final answer from the agent
        
    Returns:
        float or None: The extracted numerical value, or None if not found
    """
    if not final_answer:
        return None
    
    # Look for patterns like "is 123", "equals 456.78", "result is 789"
    patterns = [
        r'(?:is|equals?|result(?:\s+is)?)\s+(?:approximately\s+)?([+-]?\d+(?:\.\d+)?)',
        r'([+-]?\d+(?:\.\d+)?)\s*(?:square\s+units)?\.?\s*$',  # For area calculations
        r'→\s*([+-]?\d+(?:\.\d+)?)',  # For tool results
        r'([+-]?\d+(?:\.\d+))',  # Any number in the text
    ]
    
    for pattern in patterns:
        match = re.search(pattern, final_answer, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                continue
    
    return None

def extract_expression_with_llm(query):
    """Extract mathematical expression from query using LLM.
    
    Args:
        query: The user's calculation query
        
    Returns:
        str or None: The extracted mathematical expression, or None if not found
    """
    try:
        llm = configure_llm()
        
        extraction_prompt = f"""Extract the mathematical expression from this query and return ONLY the mathematical expression that can be evaluated with Python's eval() function.

Query: "{query}"

Rules:
- Return only the mathematical expression (e.g., "15 + 25", "(15 + 25) * 3", "1024 / 8")
- Use standard Python operators: +, -, *, /, **, %, //
- Use parentheses for grouping: ()
- Do not include any explanatory text
- If no clear mathematical expression exists, return "NONE"

Mathematical expression:"""
        
        response = llm.invoke([HumanMessage(content=extraction_prompt)])
        expression = response.content.strip()
        
        # Clean up the response
        if "NONE" in expression.upper() or not expression:
            return None
            
        # Remove any quotes or extra formatting
        expression = expression.strip('"\'`')
        
        # Basic validation - check if it looks like a math expression
        if any(op in expression for op in ['+', '-', '*', '/', '(', ')']):
            return expression
            
    except Exception as e:
        print(f"⚠️  Warning: Failed to extract expression with LLM: {e}")
    
    return None

def safe_eval_expression(expression):
    """Safely evaluate mathematical expression using Python's eval.
    
    Args:
        expression: Mathematical expression string
        
    Returns:
        float or None: The calculated result, or None if evaluation failed
    """
    if not expression:
        return None
    
    try:
        # Define safe operators
        safe_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.FloorDiv: operator.floordiv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        def safe_eval_node(node):
            if isinstance(node, ast.Constant):  # Numbers (Python 3.8+)
                return node.value
            elif hasattr(ast, 'Num') and isinstance(node, ast.Num):  # Python < 3.8 compatibility
                return node.n
            elif isinstance(node, ast.BinOp):  # Binary operations
                left = safe_eval_node(node.left)
                right = safe_eval_node(node.right)
                op = safe_ops.get(type(node.op))
                if op:
                    return op(left, right)
                else:
                    raise ValueError(f"Unsupported operation: {type(node.op)}")
            elif isinstance(node, ast.UnaryOp):  # Unary operations
                operand = safe_eval_node(node.operand)
                op = safe_ops.get(type(node.op))
                if op:
                    return op(operand)
                else:
                    raise ValueError(f"Unsupported unary operation: {type(node.op)}")
            else:
                raise ValueError(f"Unsupported node type: {type(node)}")
        
        # Parse and evaluate
        tree = ast.parse(expression, mode='eval')
        result = safe_eval_node(tree.body)
        return float(result)
        
    except Exception as e:
        print(f"⚠️  Warning: Failed to evaluate expression '{expression}': {e}")
        return None

def print_tool_execution_details(chunk, tool_tracker=None):
    """Print detailed information about tool execution"""
    if tool_tracker is None:
        tool_tracker = {'calls': [], 'results': [], 'pending_calls': {}, 'last_result': None}
    
    for node, data in chunk.items():
        if 'messages' in data:
            for message in data['messages']:
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        call_id = tool_call.get('id', f"{tool_call['name']}_{len(tool_tracker['calls'])}")
                        tool_tracker['calls'].append(tool_call)
                        tool_tracker['pending_calls'][call_id] = tool_call
                
                elif hasattr(message, 'invalid_tool_calls') and message.invalid_tool_calls:
                    print(f"\n❌ Invalid Tool Calls from {node}:")
                    for invalid_call in message.invalid_tool_calls:
                        print(f"   🚫 {invalid_call['name']}: {invalid_call.get('error', 'Invalid format')}")
                
                elif isinstance(message, ToolMessage):
                    result_info = {'name': message.name, 'content': message.content, 'tool_call_id': message.tool_call_id}
                    tool_tracker['results'].append(result_info)
                    
                    # Find the corresponding tool call and print the combined format
                    matching_call = None
                    if message.tool_call_id in tool_tracker['pending_calls']:
                        matching_call = tool_tracker['pending_calls'][message.tool_call_id]
                        del tool_tracker['pending_calls'][message.tool_call_id]
                    else:
                        # Fallback: find by name
                        for call_id, call in list(tool_tracker['pending_calls'].items()):
                            if call['name'] == message.name:
                                matching_call = call
                                del tool_tracker['pending_calls'][call_id]
                                break
                    
                    if matching_call:
                        print(f"🛠️  {matching_call['name']}({matching_call['args']}) -> {message.content}")
                    else:
                        print(f"🛠️  {message.name}(...) -> {message.content}")
                    
                    # Store the last result as potential final value
                    tool_tracker['last_result'] = message.content
                
                elif isinstance(message, AIMessage) and message.content and not hasattr(message, 'tool_calls'):
                    print(f"\n🤖 AI Response from {node}:")
                    print(f"   💭 {message.content}")
    
    return tool_tracker

def print_final_result(tool_tracker):
    """Print the final calculation result if available"""
    if 'last_result' in tool_tracker and tool_tracker['last_result'] is not None:
        print(f"🎯 result = {tool_tracker['last_result']}")

def print_tool_summary(tool_tracker):
    """Print a nice summary of all tool calls and their results"""
    if not tool_tracker['calls'] and not tool_tracker['results']:
        return
    
    # Create a mapping of calls to results
    call_result_pairs = []
    
    # Try to match calls with results
    calls_used = set()
    for result in tool_tracker['results']:
        # Find matching call by name (simple approach for summary)
        for i, call in enumerate(tool_tracker['calls']):
            if i not in calls_used and call['name'] == result['name']:
                call_result_pairs.append((call, result))
                calls_used.add(i)
                break
    
    # Print the matched pairs
    if call_result_pairs:
        for call, result in call_result_pairs:
            print(f"🛠️  {call['name']}({call['args']}) -> {result['content']}")
    
    # Print any remaining calls without results
    for i, call in enumerate(tool_tracker['calls']):
        if i not in calls_used:
            print(f"🛠️  {call['name']}({call['args']}) -> [pending]")
    
    # Print final result
    if 'last_result' in tool_tracker and tool_tracker['last_result'] is not None:
        print(f"🎯 result = {tool_tracker['last_result']}")

def run_calculation(agent, query, repeat=1):
    """Run a calculation query and show detailed execution with optional validation.
    
    Args:
        agent: The calculator agent to use
        query: The calculation query string
        repeat: Number of times to run the calculation for validation (default=1)
    
    Returns:
        The result from the last execution
    """
    if repeat < 1:
        repeat = 1
    
    # Extract expression and calculate ground truth for validation
    extracted_expression = extract_expression_with_llm(query)
    ground_truth = safe_eval_expression(extracted_expression) if extracted_expression else None
    
    if extracted_expression and ground_truth is not None:
        print(f"📐 Extracted expression: {extracted_expression}")
        print(f"🧮 Python eval result: {ground_truth}")
        print()
    
    results = []
    numerical_results = []
    execution_times = []
    
    # Run calculation multiple times if repeat > 1
    for run_num in range(repeat):
        if repeat > 1:
            print(f"\n{'='*60}")
            print(f"🧮 QUERY (Run {run_num + 1}/{repeat}): {query}")
            print('='*60)
        else:
            print(f"\n{'='*60}")
            print(f"🧮 QUERY: {query}")
            print('='*60)
        
        start_time = time.time()
        
        # Stream the agent execution to see tool calls
        result = None
        successful_calculation = False
        final_answer = None
        
        tool_tracker = {'calls': [], 'results': [], 'pending_calls': {}, 'last_result': None}
        for chunk in agent.stream({"messages": [HumanMessage(content=query)]}):
            if repeat == 1:  # Only show detailed output for single runs
                tool_tracker = print_tool_execution_details(chunk, tool_tracker)
            else:  # For multiple runs, just track tools without detailed printing
                for node, data in chunk.items():
                    if 'messages' in data:
                        for message in data['messages']:
                            if hasattr(message, 'tool_calls') and message.tool_calls:
                                tool_tracker['calls'].extend(message.tool_calls)
                            elif isinstance(message, ToolMessage):
                                tool_tracker['results'].append({'name': message.name, 'content': message.content})
                                tool_tracker['last_result'] = message.content
            result = chunk
            
            # Check for successful tool execution
            if 'agent' in chunk and 'messages' in chunk['agent']:
                for message in chunk['agent']['messages']:
                    if isinstance(message, ToolMessage):
                        successful_calculation = True
                        final_answer = message.content
                    elif isinstance(message, AIMessage) and message.content:
                        final_answer = message.content
        
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        
        # Store results
        results.append({
            'result': result,
            'successful_calculation': successful_calculation,
            'final_answer': final_answer,
            'execution_time': execution_time,
            'tools_used': len(tool_tracker['results']) > 0
        })
        
        # Print final result summary for single runs
        if repeat == 1:
            print_final_result(tool_tracker)
        
        # Extract numerical result for validation
        numerical_result = extract_numerical_result(final_answer)
        numerical_results.append(numerical_result)
        
        # Display result for this run
        if repeat > 1:
            # Show tool summary for multiple runs
            print_tool_summary(tool_tracker)
            
            if successful_calculation and final_answer:
                print(f"\n🎯 FINAL ANSWER (Run {run_num + 1}): {final_answer}")
                if numerical_result is not None:
                    print(f"📊 Extracted value: {numerical_result}")
            elif final_answer:
                print(f"\n🤖 FINAL RESPONSE (Run {run_num + 1}): {final_answer}")
            else:
                print(f"\n❌ No valid result obtained (Run {run_num + 1})")
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
    
    # Display final summary
    if repeat == 1:
        # Single run - display as before
        result_info = results[0]
        if result_info['final_answer']:
            print(f"\n🤖 FINAL RESPONSE: {result_info['final_answer']}")
            
            # Check if tools were actually used
            tools_were_used = result_info['tools_used']
            agent_result = numerical_results[0] if numerical_results[0] is not None else None
            
            if tools_were_used:
                # Tools were used - validate normally
                if ground_truth is not None and agent_result is not None:
                    # Use a reasonable tolerance for floating point comparison (0.01 for practical precision)
                    if abs(agent_result - ground_truth) < 0.01:
                        print(f"🔍 VALIDATION: ✅ correct")
                    else:
                        print(f"🔍 VALIDATION: ❌ wrong (Agent: {agent_result}, Python: {round(ground_truth, 6)})")
                elif ground_truth is not None:
                    print(f"🔍 VALIDATION: ⚠️ unable to extract agent result")
                elif agent_result is not None:
                    print(f"🔍 VALIDATION: ⚠️ unable to extract expression")
                else:
                    print(f"🔍 VALIDATION: ⚠️ unable to validate")
            else:
                # No tools were used
                print(f"🔍 VALIDATION: ⚠️ no tools used")
            
            print(f"✅ Calculation completed successfully!")
        else:
            print(f"\n❌ No valid result obtained")
            print(f"🔍 VALIDATION: ❌ failed")
        
        print(f"\n⏱️  Execution time: {result_info['execution_time']:.2f} seconds")
    else:
        # Multiple runs - show validation summary
        print(f"\n{'='*60}")
        print(f"📋 VALIDATION SUMMARY ({repeat} runs)")
        print('='*60)
        
        # Check consistency of numerical results
        valid_results = [r for r in numerical_results if r is not None]
        if len(valid_results) > 0:
            all_same = all(abs(r - valid_results[0]) < 1e-10 for r in valid_results)
            agent_result = valid_results[0] if valid_results else None
            
            # Compare with ground truth if available
            if ground_truth is not None and agent_result is not None:
                ground_truth_match = abs(agent_result - ground_truth) < 0.01
                
                # Also check LLM final answers across runs
                llm_results = []
                for result_info in results:
                    if result_info['final_answer']:
                        llm_result = extract_numerical_result(result_info['final_answer'])
                        if llm_result is not None:
                            llm_results.append(llm_result)
                
                llm_consistent = len(llm_results) > 0 and all(abs(r - llm_results[0]) < 1e-10 for r in llm_results)
                llm_matches_ground_truth = len(llm_results) > 0 and abs(llm_results[0] - ground_truth) < 1e-10
                
                if all_same and ground_truth_match:
                    print(f"🔍 VALIDATION: ✅ correct (all {repeat} runs consistent)")
                else:
                    print(f"🔍 VALIDATION: ❌ wrong (Agent: {agent_result}, Python: {round(ground_truth, 6)})")
                    if not all_same:
                        print(f"   • Inconsistent results: {valid_results}")
                    if not ground_truth_match:
                        print(f"   • Wrong answer: difference of {abs(agent_result - ground_truth):.6f}")
            else:
                if all_same:
                    print(f"✅ VALIDATION PASSED: All {len(valid_results)} results are consistent")
                    print(f"🎯 Consistent result: {valid_results[0]}")
                else:
                    print(f"❌ VALIDATION FAILED: Results are inconsistent")
                    print(f"📊 Results: {valid_results}")
        else:
            if ground_truth is not None:
                print(f"⚠️  VALIDATION INCONCLUSIVE: No agent results extracted")
                print(f"🧮 Python eval: {ground_truth}")
            else:
                print(f"⚠️  VALIDATION INCONCLUSIVE: No numerical results extracted")
        
        # Show execution time statistics
        avg_time = sum(execution_times) / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        print(f"\n⏱️  Execution times - Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
    
    print(f"{'='*60}")
    
    return results[-1]['result']  # Return the last result