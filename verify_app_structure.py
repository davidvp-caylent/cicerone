"""
Verification script for app.py structure.

This script verifies that app.py has the correct structure for AgentCore
deployment without requiring the bedrock-agentcore package to be installed.
"""

import ast
import sys


def verify_app_structure():
    """Verify that app.py has all required components."""
    print("\n" + "="*60)
    print("Verifying AgentCore Integration Structure")
    print("="*60 + "\n")
    
    with open('app.py', 'r') as f:
        content = f.read()
        tree = ast.parse(content)
    
    # Check for required imports
    print("✓ Checking imports...")
    required_imports = [
        'BedrockAgentCoreApp',
        'agent',
        'get_session_state',
        'save_session_state',
        'create_new_session'
    ]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in required_imports:
                    required_imports.remove(alias.name)
                    print(f"  ✓ Found import: {alias.name}")
    
    if required_imports:
        print(f"  ✗ Missing imports: {required_imports}")
        return False
    
    # Check for required functions
    print("\n✓ Checking helper functions...")
    required_functions = [
        '_extract_user_message',
        '_extract_session_id',
        '_get_or_create_session',
        '_update_session_history',
        '_format_response',
        'agent_invocation',
        'main'
    ]
    
    found_functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            found_functions.append(node.name)
            if node.name in required_functions:
                print(f"  ✓ Found function: {node.name}")
    
    missing_functions = set(required_functions) - set(found_functions)
    if missing_functions:
        print(f"  ✗ Missing functions: {missing_functions}")
        return False
    
    # Check for decorator on agent_invocation
    print("\n✓ Checking decorators...")
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'agent_invocation':
            if node.decorator_list:
                print(f"  ✓ agent_invocation has decorator")
            else:
                print(f"  ✗ agent_invocation missing @app.entrypoint decorator")
                return False
    
    # Check for environment variables
    print("\n✓ Checking environment configuration...")
    env_vars = ['AWS_REGION', 'BEDROCK_MODEL_ID', 'LOG_LEVEL']
    for var in env_vars:
        if var in content:
            print(f"  ✓ Found env var: {var}")
    
    # Check for error handling
    print("\n✓ Checking error handling...")
    has_try_except = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            has_try_except = True
            break
    
    if has_try_except:
        print(f"  ✓ Error handling implemented")
    else:
        print(f"  ✗ No error handling found")
        return False
    
    # Check for logging
    print("\n✓ Checking logging...")
    if 'logging' in content and 'logger' in content:
        print(f"  ✓ Logging configured")
    else:
        print(f"  ✗ Logging not configured")
        return False
    
    print("\n" + "="*60)
    print("✓ All structure checks passed!")
    print("="*60)
    print("\nThe app.py file is correctly structured for AgentCore deployment.")
    print("\nNext steps:")
    print("1. Install bedrock-agentcore: pip install bedrock-agentcore")
    print("2. Configure AWS credentials in .env file")
    print("3. Test locally: python app.py")
    print("4. Deploy using: agentcore configure --entrypoint app.py && agentcore launch")
    print("\nSee DEPLOYMENT.md for detailed deployment instructions.")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = verify_app_structure()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
