# LLM Pentesting Tools

A toolkit for testing and evaluating the security of Large Language Models (LLMs) against various types of attacks.

## Installation

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root with your chosen provider's configuration. Example configuration for all supported providers:

```ini
# LLM Provider Selection
# Options: openai, cohere, anthropic, google, mistral, azure_openai, huggingface, replicate
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4  # Options: gpt-4, gpt-3.5-turbo, gpt-4-turbo-preview

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key
COHERE_MODEL=command  # Options: command, command-light, command-nightly

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_MODEL=claude-3-opus  # Options: claude-3-opus, claude-3-sonnet, claude-2.1

# Google Configuration
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-pro  # Options: gemini-pro, gemini-pro-vision

# Mistral Configuration
MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_MODEL=mistral-large  # Options: mistral-tiny, mistral-small, mistral-medium, mistral-large

# Azure OpenAI Configuration
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_MODEL=your_model_deployment
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Hugging Face Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key
HUGGINGFACE_MODEL=your_model_id  # e.g., meta-llama/Llama-2-70b-chat-hf

# Replicate Configuration
REPLICATE_API_KEY=your_replicate_api_key
REPLICATE_MODEL=your_model_version  # e.g., replicate/llama-2-70b-chat
```

You only need to configure the provider you plan to use. Set `LLM_PROVIDER` to your chosen provider and fill in the corresponding API keys and model settings.

## Usage

Basic usage with default provider (OpenAI):

```bash
python run_test.py --attack-type prompt_injection
```

Specify a different provider:

```bash
python run_test.py --provider cohere --attack-type prompt_injection
```

Available providers:
- `openai` (default) - OpenAI GPT models
- `cohere` - Cohere Command models
- `anthropic` - Anthropic Claude models
- `google` - Google Gemini models
- `mistral` - Mistral AI models
- `azure_openai` - Azure-hosted OpenAI models
- `huggingface` - Hugging Face model deployments
- `replicate` - Replicate.com model deployments

Additional options:
```bash
# Force reload of .env file
python run_test.py --force-reload

# Specify custom .env file
python run_test.py --env-file /path/to/custom.env

# Enable verbose logging
python run_test.py --verbose

# Save results to file
python run_test.py --save-results
```

## Attack Types

The toolkit supports the following types of attacks:

- `prompt_injection`: Tests for prompt injection vulnerabilities
- `prompt_leaking`: Tests for leaking of prompt information
- `junction_attack`: Tests for junction-based attacks
- `code_injection`: Tests for code injection vulnerabilities
- `role_playing`: Tests for role-playing based attacks
- `system_prompt_extraction`: Tests for extracting system prompts
- `jailbreak`: Tests for jailbreak attempts
- `data_extraction`: Tests for extracting sensitive data
- `model_extraction`: Tests for extracting model information
- `system_prompt`: Tests system prompt manipulation
- `token_smuggling`: Tests for token smuggling attacks

Example usage:
```bash
python run_test.py --attack-type jailbreak --provider cohere
```

## Project Structure

```
llm_pentest/
├── attacks/           # Attack implementations
├── data/             # Attack data and templates
├── output/           # Test results and reports
├── utils/            # Utility functions
├── config.py         # Configuration management
└── __init__.py       # Package initialization
```

## Provider-Specific Notes

### Azure OpenAI
When using Azure OpenAI, make sure to set both the endpoint and deployment name in your `.env` file. The API version will default to the latest supported version if not specified.

### Hugging Face
For Hugging Face, you'll need to specify the full model ID (e.g., `meta-llama/Llama-2-70b-chat-hf`). Make sure you have the necessary model access permissions.

### Replicate
For Replicate, specify the model version string as found in the Replicate model page (e.g., `replicate/llama-2-70b-chat`).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Try different attack types
python run_test.py --attack-type prompt_injection --provider cohere --verbose
python run_test.py --attack-type data_extraction --provider cohere --verbose
python run_test.py --attack-type model_extraction --provider cohere --verbose

