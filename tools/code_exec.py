"""
Code Execution Tool for Jarvis
Execute Python code snippets safely in a restricted environment
"""
from langchain.tools import tool
import sys
import io
import logging
from contextlib import redirect_stdout, redirect_stderr
import traceback


@tool
def execute_python_code(code: str) -> str:
    """
    Execute Python code safely and return the output.
    
    Args:
        code: Python code to execute
    
    Examples:
        - "Calculate 15 * 24"
        - "Run: print('Hello World')"
        - "Execute: sum([1, 2, 3, 4, 5])"
    
    Returns:
        Code execution output or error message
    
    Security Notes:
        - Limited to basic Python operations
        - No file system access
        - No network access
        - No subprocess calls
    """
    try:
        # Security restrictions
        restricted_keywords = [
            'import os', 'import sys', 'import subprocess',
            'open(', '__import__', 'exec(', 'eval(',
            'compile(', 'globals()', 'locals()',
            '__builtins__', '__class__', '__dict__'
        ]
        
        for keyword in restricted_keywords:
            if keyword in code:
                return f"❌ Security Error: '{keyword}' is not allowed"
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # Create restricted namespace
        safe_builtins = {
            'abs': abs, 'all': all, 'any': any, 'bin': bin,
            'bool': bool, 'chr': chr, 'dict': dict, 'divmod': divmod,
            'enumerate': enumerate, 'filter': filter, 'float': float,
            'format': format, 'hex': hex, 'int': int, 'isinstance': isinstance,
            'len': len, 'list': list, 'map': map, 'max': max,
            'min': min, 'oct': oct, 'ord': ord, 'pow': pow,
            'print': print, 'range': range, 'reversed': reversed,
            'round': round, 'set': set, 'slice': slice, 'sorted': sorted,
            'str': str, 'sum': sum, 'tuple': tuple, 'type': type,
            'zip': zip
        }
        
        namespace = {'__builtins__': safe_builtins}
        
        # Execute code with redirected output
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            # Try to evaluate as expression first
            try:
                result = eval(code, namespace)
                if result is not None:
                    print(result)
            except SyntaxError:
                # If not an expression, execute as statement
                exec(code, namespace)
        
        # Get output
        stdout_text = stdout_capture.getvalue()
        stderr_text = stderr_capture.getvalue()
        
        if stderr_text:
            return f"⚠️ Execution Error:\n{stderr_text}"
        
        if stdout_text:
            return f"✅ Output:\n{stdout_text.strip()}"
        else:
            return "✅ Code executed successfully (no output)"
            
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"Code execution error: {error_trace}")
        return f"❌ Error:\n{str(e)}\n\nTraceback:\n{error_trace}"


@tool
def calculate_expression(expression: str) -> str:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: Mathematical expression to calculate
    
    Examples:
        - "Calculate 15 * 24"
        - "What is 2^10?"
        - "Evaluate (5 + 3) * 2"
    
    Returns:
        Calculation result
    """
    try:
        # Allow basic math operations
        safe_builtins = {
            'abs': abs, 'pow': pow, 'round': round,
            'min': min, 'max': max, 'sum': sum
        }
        
        # Replace ** with pow for safety
        expression = expression.replace('^', '**')
        
        # Evaluate expression
        result = eval(expression, {"__builtins__": safe_builtins})
        
        return f"🔢 {expression} = {result}"
        
    except Exception as e:
        logging.error(f"Calculation error: {e}")
        return f"❌ Calculation error: {str(e)}"


@tool
def run_python_script(script_content: str, description: str = "") -> str:
    """
    Run a longer Python script with multiple lines.
    
    Args:
        script_content: Multi-line Python script
        description: Optional description of what the script does
    
    Examples:
        - "Run a for loop to print numbers 1-10"
        - "Create a function to calculate factorial"
    
    Returns:
        Script execution output
    """
    try:
        logging.info(f"Running script: {description or 'No description'}")
        
        # Use the execute_python_code tool
        result = execute_python_code.invoke({"code": script_content})
        
        if description:
            return f"📝 Script: {description}\n\n{result}"
        else:
            return result
            
    except Exception as e:
        logging.error(f"Script execution error: {e}")
        return f"❌ Script error: {str(e)}"


@tool
def create_data_visualization(data_description: str) -> str:
    """
    Create simple text-based data visualizations.
    
    Args:
        data_description: Description of data to visualize
    
    Examples:
        - "Create a bar chart of [10, 20, 15, 30]"
        - "Visualize these numbers: 5, 10, 15"
    
    Returns:
        ASCII art visualization
    """
    try:
        # Extract numbers from description
        import re
        numbers = [int(x) for x in re.findall(r'\d+', data_description)]
        
        if not numbers:
            return "❌ No numbers found in description"
        
        # Create simple bar chart
        max_val = max(numbers)
        chart_lines = []
        chart_lines.append("📊 Simple Bar Chart:")
        chart_lines.append("")
        
        for i, val in enumerate(numbers):
            bar_length = int((val / max_val) * 40)  # Scale to 40 chars
            bar = '█' * bar_length
            chart_lines.append(f"[{i+1}] {bar} {val}")
        
        return "\n".join(chart_lines)
        
    except Exception as e:
        logging.error(f"Visualization error: {e}")
        return f"❌ Visualization error: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Code execution tools created. Testing...")
    
    # Test calculation
    result1 = calculate_expression.invoke({"expression": "15 * 24"})
    print(result1)
    
    # Test simple code
    result2 = execute_python_code.invoke({"code": "print('Hello from Jarvis!')"})
    print(result2)
    
    # Test visualization
    result3 = create_data_visualization.invoke({"data_description": "numbers: 10, 20, 15, 30"})
    print(result3)
