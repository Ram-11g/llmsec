import logging
from pentest import AttackGenerator, LLMAttacker, AttackType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Initialize components
    attack_generator = AttackGenerator()
    llm_attacker = LLMAttacker(
        endpoint="http://your-llm-endpoint/v1/chat/completions",
        headers={"Authorization": "Bearer your-token"}  # Optional
    )

    # Example 1: Run a single attack
    print("\nRunning single attack...")
    result = llm_attacker.test_prompt_injection(
        base_prompt="You are a helpful AI assistant."
    )
    print(f"Attack successful: {result.success}")
    print(f"Response: {result.response[:100]}...")

    # Example 2: Run all attacks
    print("\nRunning all attacks...")
    results = llm_attacker.run_all_attacks(
        base_prompt="You are a helpful AI assistant."
    )
    for result in results:
        print(f"\n{result.attack_type.value}:")
        print(f"Success: {result.success}")
        print(f"Response: {result.response[:100]}...")

    # Example 3: Collect data and generate attack
    print("\nCollecting data and generating attack...")
    attack_generator.update_data([
        "LLM security",
        "LLM vulnerabilities",
        "LLM attacks"
    ])
    
    payload = attack_generator.generate_attack_payload(
        attack_type=AttackType.PROMPT_INJECTION.value,
        base_prompt="You are a helpful AI assistant."
    )
    print(f"Generated payload: {payload[:100]}...")

if __name__ == "__main__":
    main() 