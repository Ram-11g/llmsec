from llm_pentest.attacks.llm_attacker import LLMAttacker, AttackType
from llm_pentest.config import LLMProvider, CURRENT_PROVIDER
import logging
import argparse
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import json
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_env_variables(env_path: Path = None, force_reload: bool = False) -> bool:
    """Load environment variables from .env file with optional force reload."""
    try:
        if env_path is None:
            env_path = find_dotenv(raise_error_if_not_found=True)
        elif isinstance(env_path, str):
            env_path = Path(env_path)
        
        # Check if .env file exists and get its last modification time
        if env_path.exists():
            current_mtime = env_path.stat().st_mtime
            last_load_time = getattr(load_env_variables, 'last_load_time', 0)
            
            # Reload if forced or if file has been modified
            if force_reload or current_mtime > last_load_time:
                load_dotenv(env_path, override=True)
                load_env_variables.last_load_time = current_mtime
                logger.info(f"Loaded/Reloaded environment variables from {env_path}")
                return True
            else:
                logger.debug("Using cached environment variables")
                return False
        else:
            logger.warning(f".env file not found at {env_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading environment variables: {str(e)}")
        return False

def save_results(results: dict, output_dir: Path):
    """Save attack results to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"attack_results_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {output_file}")

def validate_environment(provider: str) -> bool:
    """Validate that all required environment variables are set for the given provider."""
    required_vars = {
        LLMProvider.OPENAI.value: ["OPENAI_API_KEY"],
        LLMProvider.COHERE.value: ["COHERE_API_KEY"],
        LLMProvider.ANTHROPIC.value: ["ANTHROPIC_API_KEY"],
        LLMProvider.GOOGLE.value: ["GOOGLE_API_KEY"],
        LLMProvider.MISTRAL.value: ["MISTRAL_API_KEY"]
    }
    
    missing_vars = []
    for var in required_vars.get(provider, []):
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables for {provider}: {', '.join(missing_vars)}")
        return False
    
    return True

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run LLM Penetration Tests')
    parser.add_argument('--attack-type', type=str, default='prompt_injection',
                      choices=[attack.value for attack in AttackType],
                      help='Type of attack to run')
    parser.add_argument('--provider', type=str, default='openai',
                      choices=[provider.value for provider in LLMProvider],
                      help='LLM provider to test against')
    parser.add_argument('--base-prompt', type=str, default='Tell me about yourself',
                      help='Base prompt to use for testing')
    parser.add_argument('--output-dir', type=str, default='output',
                      help='Directory to save results')
    parser.add_argument('--save-results', action='store_true',
                      help='Save results to JSON file')
    parser.add_argument('--verbose', action='store_true',
                      help='Enable verbose logging')
    parser.add_argument('--env-file', type=str, default=None,
                      help='Path to .env file (default: auto-detect)')
    parser.add_argument('--force-reload', action='store_true',
                      help='Force reload of .env file')
    args = parser.parse_args()

    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load environment variables
    env_path = Path(args.env_file) if args.env_file else None
    if not load_env_variables(env_path, args.force_reload):
        logger.warning("Using existing environment variables")

    # Validate environment for the selected provider
    if not validate_environment(args.provider):
        raise ValueError(f"Missing required environment variables for {args.provider}")

    # Set the provider in environment
    os.environ['LLM_PROVIDER'] = args.provider

    # Create necessary directories
    data_dir = Path("data")
    output_dir = Path(args.output_dir)
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    try:
        # Initialize the attacker
        logger.info(f"Initializing LLM attacker for {args.provider}...")
        logger.debug(f"Using API endpoint: {CURRENT_PROVIDER['api_url']}")
        logger.debug(f"Using model: {CURRENT_PROVIDER['model']}")
        
        attacker = LLMAttacker(data_dir=str(data_dir))

        # Run the specified attack
        logger.info(f"Running {args.attack_type} attack against {args.provider}...")
        logger.info(f"Base prompt: {args.base_prompt}")
        
        try:
            attack_type = AttackType(args.attack_type)
            result = attacker.run_specific_attack(attack_type, args.base_prompt)
        except ValueError as e:
            logger.error(f"Invalid attack type: {args.attack_type}")
            logger.error(f"Valid attack types are: {[attack.value for attack in AttackType]}")
            raise

        # Prepare results
        results = {
            "timestamp": datetime.now().isoformat(),
            "provider": args.provider,
            "attack_type": result.attack_type.value,
            "success": result.success,
            "response": result.response,
            "execution_time": result.execution_time,
            "payload": result.payload,
            "error": result.error,
            "environment": {
                "api_url": CURRENT_PROVIDER['api_url'],
                "model": CURRENT_PROVIDER['model'],
                "env_file": str(env_path) if env_path else None,
                "env_loaded": bool(env_path and env_path.exists())
            }
        }

        # Print results
        print("\nAttack Results:")
        print(f"Provider: {args.provider}")
        print(f"Attack Type: {result.attack_type.value}")
        print(f"Success: {result.success}")
        print(f"Response: {result.response}")
        print(f"Execution Time: {result.execution_time:.2f}s")
        if result.error:
            print(f"Error: {result.error}")

        # Save results if requested
        if args.save_results:
            save_results(results, output_dir)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        if args.verbose:
            logger.exception("Detailed error traceback:")
        raise

if __name__ == "__main__":
    main() 