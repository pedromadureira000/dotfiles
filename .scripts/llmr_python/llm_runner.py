import llm
import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from enum import Enum
import logging # For llm library's own logging control if needed
import argparse
import sys

# Configure llm library logging if it's too verbose by default
# logging.getLogger("llm").setLevel(logging.WARNING)

# --- IMPORTANT ---
# For these examples to run, you need:
# 1. `llm` library installed (`pip install llm`)
# 2. Model-specific plugins installed (e.g., `pip install llm-openai llm-gemini llm-claude`)
# 3. API keys set as environment variables:
#    export OPENAI_API_KEY="sk-..."
#    export GOOGLE_API_KEY="..." (for llm-gemini, or LLM_GEMINI_KEY depending on plugin version)
#    export ANTHROPIC_API_KEY="..."



class LLMExecutionType(Enum):
    MODEL_NON_STREAM = "run_model_non_stream"
    MODEL_STREAM = "run_model_stream"
    ASYNC_MODEL_NON_STREAM = "run_async_model_no_stream"
    ASYNC_MODEL_STREAM = "run_async_model_stream"

class LLMRunner:
    def __init__(self, base_folder: str = "~/utils/llmr_py_runs", default_mode: str = "default"):
        self.base_folder = Path(base_folder).expanduser()
        self.default_mode = default_mode
        self.api_keys = {
            "gemini": os.environ.get("LLM_GEMINI_KEY") or os.environ.get("GOOGLE_API_KEY"),
            "openai": os.environ.get("OPENAI_API_KEY"),
            "claude": os.environ.get("ANTHROPIC_API_KEY"),
        }

    def _get_api_key(self, model_type: str):
        key = self.api_keys.get(model_type.lower())
        if not key:
            print(f"Warning: API key for {model_type} not found in environment variables.")
        return key

    def _calculate_pricing(self, model_name_used: str, input_tokens: int, output_tokens: int, total_tokens: int = None):
        input_price_val = 0.0
        output_price_val = 0.0
        model_info_str = ""
        model_name_lower = model_name_used.lower()

        # Pricing based on bash script and common models
        # Ensure these are up-to-date with actual costs
        if "gemini" in model_name_lower:
            # Example: gemini-1.5-pro-latest vs gemini-1.5-flash-latest
            if "flash" in model_name_lower: # Gemini 1.5 Flash
                input_price_val = (input_tokens / 1_000_000) * 0.35 
                output_price_val = (output_tokens / 1_000_000) * 0.70 # Adjusted from $1.05 to $0.70 for Flash example
            elif "gemini-1.0-pro" in model_name_lower: # Older Gemini Pro
                input_price_val = (input_tokens / 1_000_000) * 0.50
                output_price_val = (output_tokens / 1_000_000) * 1.50
            else: # Default to Gemini 1.5 Pro pricing
                input_price_val = (input_tokens / 1_000_000) * 3.50 
                output_price_val = (output_tokens / 1_000_000) * 10.50
            model_info_str = dedent(f"""
              **gemini usage ({model_name_used})**:
                - input_tokens: {input_tokens} (price: ${input_price_val:.6f})
                - output_tokens: {output_tokens} (price: ${output_price_val:.6f})
            """).strip()
        elif "gpt" in model_name_lower or "openai" in model_name_lower:
            if "gpt-4o-mini" in model_name_lower:
                input_price_val = (input_tokens / 1_000_000) * 0.15
                output_price_val = (output_tokens / 1_000_000) * 0.60
            elif "gpt-4o" in model_name_lower and not "mini" in model_name_lower: # gpt-4o (full)
                input_price_val = (input_tokens / 1_000_000) * 5.00
                output_price_val = (output_tokens / 1_000_000) * 15.00
            elif "gpt-4-turbo" in model_name_lower or "gpt-4.1" in model_name_lower : # Covers gpt-4-turbo, gpt-4-turbo-preview, etc.
                input_price_val = (input_tokens / 1_000_000) * 10.00
                output_price_val = (output_tokens / 1_000_000) * 30.00
            elif "gpt-3.5-turbo" in model_name_lower:
                input_price_val = (input_tokens / 1_000_000) * 0.50
                output_price_val = (output_tokens / 1_000_000) * 1.50
            else: # Fallback for other OpenAI models
                input_price_val = (input_tokens / 1_000_000) * 1.00 
                output_price_val = (output_tokens / 1_000_000) * 3.00
            
            effective_total_tokens = total_tokens if total_tokens is not None else input_tokens + output_tokens
            model_info_str = dedent(f"""
              **openai usage ({model_name_used})**:
                - input_tokens: {input_tokens} (price: ${input_price_val:.6f})
                - output_tokens: {output_tokens} (price: ${output_price_val:.6f})
                - total_tokens: {effective_total_tokens}
            """).strip()
        elif "claude" in model_name_lower:
            if "sonnet" in model_name_lower: # Claude 3/3.5/3.7 Sonnet
                input_price_val = (input_tokens / 1_000_000) * 3.00
                output_price_val = (output_tokens / 1_000_000) * 15.00
            elif "haiku" in model_name_lower: # Claude 3 Haiku
                input_price_val = (input_tokens / 1_000_000) * 0.25
                output_price_val = (output_tokens / 1_000_000) * 1.25
            elif "opus" in model_name_lower: # Claude 3 Opus
                input_price_val = (input_tokens / 1_000_000) * 15.00
                output_price_val = (output_tokens / 1_000_000) * 75.00
            else: # Fallback for other Claude models
                input_price_val = (input_tokens / 1_000_000) * 3.00
                output_price_val = (output_tokens / 1_000_000) * 15.00
            model_info_str = dedent(f"""
              **claude usage ({model_name_used})**:
                - input_tokens: {input_tokens} (price: ${input_price_val:.6f})
                - output_tokens: {output_tokens} (price: ${output_price_val:.6f})
            """).strip()
        else:
            effective_total_tokens = total_tokens if total_tokens is not None else input_tokens + output_tokens
            model_info_str = dedent(f"""
              **Unknown model usage ({model_name_used})**:
                - input_tokens: {input_tokens}
                - output_tokens: {output_tokens}
                - total_tokens: {effective_total_tokens}
            """).strip()

        return model_info_str

    def _save_logs(self, mode: str, prompt_text_with_system: str, llm_response_obj: llm.Response, full_response_text: str):
        mode_folder = self.base_folder / mode
        log_folder = mode_folder / "log"
        log_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = log_folder / f"{timestamp}.md"
        last_log_file = mode_folder / "last-log.md"
        output_file = mode_folder / "output.md"

        #  if llm_response_obj and hasattr(llm_response_obj, 'id') and hasattr(llm_response_obj, 'model') and hasattr(llm_response_obj, 'usage'):
        print(f"▶️"*16, f"llm_response_obj: {llm_response_obj}")
        llm_internal_id = "<No ID Found>"
        if hasattr(llm_response_obj, 'id'):
            llm_internal_id = llm_response_obj.id
        model_name_actually_used = "<model-name-missing>" # TODO FIXME should take this from selected model instead
        if hasattr(llm_response_obj, 'model'):
            model_name_actually_used = llm_response_obj.model.model_id
        
        api_response_json = {}
        if hasattr(llm_response_obj, 'json') and callable(llm_response_obj.json):
            try:
                api_response_json = llm_response_obj.json() or {}
            except Exception:
                api_response_json = {}

        api_specific_response_id = api_response_json.get('id', "N/A")
        object_type = api_response_json.get('object', "N/A")

        input_tokens = 0
        output_tokens = 0
        if hasattr(llm_response_obj, 'usage'):
            input_tokens = getattr(llm_response_obj.usage, 'prompt_tokens', 0) or 0
            output_tokens = getattr(llm_response_obj.usage, 'completion_tokens', 0) or 0
        
        total_tokens_from_api = None
        if 'usage' in api_response_json and isinstance(api_response_json.get('usage'), dict):
            total_tokens_from_api = api_response_json['usage'].get('total_tokens')
        pricing_info_str = "<didn't manage to get price>"
        if model_name_actually_used != "<model-name-missing>":
            try:
                pricing_info_str = self._calculate_pricing(model_name_actually_used, input_tokens, output_tokens, total_tokens_from_api)
            except Exception as err:
                print(f"▶️"*16, f"Didn't managed to get prices info")
                pricing_info_str = "<Didn't managed to get prices info>"
        
        if "openai" in model_name_actually_used.lower() and object_type != "N/A":
            pricing_info_str = f"**Object type**: {object_type}\n{pricing_info_str}"

        log_content = dedent(f"""
            # llm internal id: {llm_internal_id}
            **Model**: {model_name_actually_used}
            **API Response id**: {api_specific_response_id}
            {pricing_info_str}

            # Input:
            ```
            {prompt_text_with_system}
            ```

            # Output:
            {full_response_text}
        """).strip()

        output_file.write_text(full_response_text, encoding='utf-8')
        last_log_file.write_text(log_content, encoding='utf-8')
        log_file.write_text(log_content, encoding='utf-8')

        print(f"Output saved to: {output_file}")
        print(f"Log saved to: {log_file}")
        print(f"Last log updated: {last_log_file}")

    async def _get_response_object_from_logs(self, model_instance, full_response_text):
        # Helper to fetch last log entry and construct a mock Response object
        # This is a fallback for async streaming where Response object isn't directly available
        try:
            logs_db = llm.get_logs_db() # type: ignore
            # Query for the most recent response, ideally matching the model and part of the prompt if possible
            # For simplicity, just taking the very last one. This could be fragile.
            cursor = logs_db.execute(
                "SELECT id, response_json, prompt_tokens, completion_tokens, model_id FROM responses ORDER BY rowid DESC LIMIT 1"
            )
            last_log_row = cursor.fetchone()
            if last_log_row:
                usage_obj = llm.Usage(prompt_tokens=last_log_row["prompt_tokens"], completion_tokens=last_log_row["completion_tokens"])
                
                class MockResponseFromLog:
                    def __init__(self, log_id, model_inst, usage, response_json_str, text_val):
                        self.id = log_id
                        self.model = model_inst # The Model instance used for the call
                        self.usage = usage
                        self._response_json_str = response_json_str
                        self._text = text_val
                    
                    def json(self):
                        return json.loads(self._response_json_str) if self._response_json_str else {}
                    def text(self):
                        return self._text

                return MockResponseFromLog(
                    log_id=last_log_row["id"],
                    model_inst=model_instance,
                    usage=usage_obj,
                    response_json_str=last_log_row["response_json"],
                    text_val=full_response_text
                )
        except Exception as e:
            print(f"Warning: Could not retrieve detailed logs for async stream from DB: {e}")
        return None

    async def _handle_async_stream(self, model_instance, prompt_args_dict: dict):
        response_chunks = []
        # The prompt() method itself is an async generator here
        async_prompt_gen = model_instance.prompt(**prompt_args_dict)
        async for chunk in async_prompt_gen:
            print(str(chunk), end="", flush=True)
            response_chunks.append(str(chunk))
        print() 
        full_response_text = "".join(response_chunks)
        # XXX Disabled for now. Since don't work
        #  llm_response_obj = await self._get_response_object_from_logs(model_instance, full_response_text)
        llm_response_obj = {}
        return full_response_text, llm_response_obj

    async def _handle_async_non_stream(self, model_instance, prompt_args_dict: dict):
        async_response_obj = await model_instance.prompt(**prompt_args_dict) # This is an AsyncResponse
        
        full_response_text = await async_response_obj.text()
        print(full_response_text)
        usage_info = await async_response_obj.usage()
        
        # Wrap AsyncResponse to behave like a sync Response for logging
        class SyncedResponseWrapper:
            def __init__(self, async_resp, text_val, usage_val):
                self.id = async_resp.id
                self.model = async_resp.model # This is the Model instance
                self.usage = usage_val
                self._async_response = async_resp 
                self._text = text_val
            
            def json(self): # Attempt to get .response_json if available
                if hasattr(self._async_response, 'response_json') and self._async_response.response_json:
                    return self._async_response.response_json
                # Fallback: try to get it from logs if not directly on async_response
                # This part is complex as AsyncResponse might not store it directly.
                # For now, we rely on what AsyncResponse provides or what _get_response_object_from_logs might do.
                # The _save_logs method will try .json() and handle failure.
                print("Warning: .json() on SyncedResponseWrapper might be incomplete for async non-stream if not directly on AsyncResponse.")
                return {} # Or try to fetch from logs like in _get_response_object_from_logs

            def text(self):
                return self._text

        return full_response_text, SyncedResponseWrapper(async_response_obj, full_response_text, usage_info)

    def _run_model(self, model_name: str, model_type: str, execution_type: LLMExecutionType, 
                   prompt_text: str, mode_for_logging: str = None, **kwargs):
        current_mode = mode_for_logging if mode_for_logging is not None else self.default_mode
        
        api_key_to_use = kwargs.pop('key', self._get_api_key(model_type))
        if not api_key_to_use and not llm.get_model(model_name).needs_key == False: # Check if model actually needs a key
            print(f"API key for {model_type} ({model_name}) is missing and model requires a key. Aborting.")
            return None, None

        is_async = execution_type in [LLMExecutionType.ASYNC_MODEL_STREAM, LLMExecutionType.ASYNC_MODEL_NON_STREAM]
        
        model_instance = llm.get_model(model_name) if not is_async else llm.get_async_model(model_name)

        prompt_args = {"prompt": prompt_text}
        if api_key_to_use: # Only add key if it's available
             prompt_args["key"] = api_key_to_use
        
        system_prompt_text = kwargs.get("system")
        full_prompt_for_log = f"System: {system_prompt_text}\nUser: {prompt_text}" if system_prompt_text else f"User: {prompt_text}"


        # Common params from kwargs
        common_llm_params = ["system", "temperature", "attachments", "conversation", "max_output_tokens", "top_p", "top_k", "schema"]
        for param in common_llm_params:
            if param in kwargs:
                prompt_args[param] = kwargs.pop(param)
        
        # Model-specific params (remaining in kwargs)
        # Special handling for Claude's max_tokens vs max_output_tokens
        if "claude" in model_name.lower():
            if "max_output_tokens" in prompt_args and "max_tokens" not in kwargs: # User sent max_output_tokens
                kwargs["max_tokens"] = prompt_args.pop("max_output_tokens")
            elif "max_output_tokens" in prompt_args and "max_tokens" in kwargs: # User sent both
                 del prompt_args["max_output_tokens"] # Prefer explicit max_tokens for Claude

        prompt_args.update(kwargs) # Add remaining specific args like thinking, json_object, etc.

        full_response_text = ""
        llm_response_obj = None # This will be llm.Response or a compatible wrapper

        print(f"▶️"*16, f"{model_name}; {execution_type}; {prompt_args}; ")
        if execution_type == LLMExecutionType.MODEL_NON_STREAM:
            llm_response_obj = model_instance.prompt(**prompt_args)
            full_response_text = llm_response_obj.text()
            print(full_response_text)
        elif execution_type == LLMExecutionType.MODEL_STREAM:
            response_chunks = []
            stream_iterator = model_instance.prompt(**prompt_args)
            for chunk in stream_iterator:
                print(str(chunk), end="", flush=True)
                response_chunks.append(str(chunk))
            print()
            full_response_text = "".join(response_chunks)
            if hasattr(stream_iterator, 'response') and stream_iterator.response:
                llm_response_obj = stream_iterator.response
            else: # Fallback for streams that don't set .response
                print("[Note: .response attribute not found on stream iterator, attempting to fetch last log for details.]")
                # This needs to be async if _get_response_object_from_logs is async
                # For sync stream, we'd need a sync version or accept limitation.
                # For now, let's assume _get_response_object_from_logs can be called carefully or adapted.
                # Simplified: run a sync version of log fetching if possible or accept limited logging.
                # For this path, we'll try a simplified sync fetch if possible, or log without full details.

                # Disabled ....
                #  llm_response_obj = asyncio.run(self._get_response_object_from_logs(model_instance, full_response_text))
                llm_response_obj = {}

        elif execution_type == LLMExecutionType.ASYNC_MODEL_NON_STREAM:
            full_response_text, llm_response_obj = asyncio.run(self._handle_async_non_stream(model_instance, prompt_args))
        elif execution_type == LLMExecutionType.ASYNC_MODEL_STREAM:
            full_response_text, llm_response_obj = asyncio.run(self._handle_async_stream(model_instance, prompt_args))
        try: 
            self._save_logs(current_mode, full_prompt_for_log, llm_response_obj, full_response_text)
        except Exception as err:
            print(f"▶️"*16, f"\n")
            print(f"▶️"*16, f"Didn't manage to save logs. Got error: {err}")
        return full_response_text, llm_response_obj

    def run_openai(self, model_name: str, execution_type: LLMExecutionType, prompt: str, mode: str = None,
                   system: str = None, temperature: float = None, attachments: list = None, conversation = None,
                   max_output_tokens: int = None, top_p: float = None, schema: dict = None, key: str = None, **kwargs):
        all_args = {**locals(), **kwargs}
        del all_args['self'], all_args['kwargs'] # Remove self and kwargs from the dict to avoid duplication
        # Filter out None values to avoid passing them explicitly if not set
        run_args = {k: v for k, v in all_args.items() if k not in ['model_name', 'model_type', 'execution_type', 'prompt', 'mode'] and v is not None}
        
        return self._run_model(model_name=model_name, model_type="openai", execution_type=execution_type,
                               prompt_text=prompt, mode_for_logging=mode, **run_args)

    def run_gemini(self, model_name: str, execution_type: LLMExecutionType, prompt: str, mode: str = None,
                   system: str = None, temperature: float = None, attachments: list = None, conversation = None,
                   max_output_tokens: int = None, top_p: float = None, top_k: int = None,
                   json_object: bool = None, schema: dict = None, key: str = None, **kwargs):
        all_args = {**locals(), **kwargs}
        del all_args['self'], all_args['kwargs']
        run_args = {k: v for k, v in all_args.items() if k not in ['model_name', 'model_type', 'execution_type', 'prompt', 'mode'] and v is not None}

        return self._run_model(model_name=model_name, model_type="gemini", execution_type=execution_type,
                               prompt_text=prompt, mode_for_logging=mode, **run_args)

    def run_claude(self, model_name: str, execution_type: LLMExecutionType, prompt: str, mode: str = None,
                   system: str = None, temperature: float = None, attachments: list = None, conversation = None,
                   max_tokens: int = None, top_p: float = None, top_k: int = None, schema: dict = None,
                   thinking: bool = None, thinking_budget: int = None,
                   prefill: str = None, hide_prefill: bool = None, stop_sequences: list = None, key: str = None, **kwargs):
        all_args = {**locals(), **kwargs}
        del all_args['self'], all_args['kwargs']
        run_args = {k: v for k, v in all_args.items() if k not in ['model_name', 'model_type', 'execution_type', 'prompt', 'mode'] and v is not None}
        
        # Ensure 'max_tokens' is used for Claude if 'max_output_tokens' was intended
        if 'max_output_tokens' in run_args and 'max_tokens' not in run_args:
            run_args['max_tokens'] = run_args.pop('max_output_tokens')
        elif 'max_output_tokens' in run_args and 'max_tokens' in run_args and run_args.get('max_output_tokens') is not None:
             # If both are somehow passed and max_output_tokens has a value, prioritize max_tokens by removing the other
             if run_args.get('max_tokens') is None: # if max_tokens was None but max_output_tokens was not
                 run_args['max_tokens'] = run_args.pop('max_output_tokens')
             else: # both have values, prefer max_tokens
                 del run_args['max_output_tokens']


        return self._run_model(model_name=model_name, model_type="claude", execution_type=execution_type,
                               prompt_text=prompt, mode_for_logging=mode, **run_args)

runner = LLMRunner(default_mode="general_tests")
simple_prompt = "Tell me a very short joke."

system_prompt="You must be concise"

prompt_for_json_request = dedent("""
    Describe a dog with its name, age, breed, and one defining personality trait.
""").strip()

system_prompt_for_json_request = dedent("""
    You are a helpful assistant specialized in providing information about pets.
""").strip()


json_schema = {
    "properties": {
        "name": {"title": "Name", "type": "string", "description": "The name of the dog"},
        "age": {"title": "Age", "type": "integer", "description": "The age of the dog in years"},
        "breed": {"title": "Breed", "type": "string", "description": "The breed of the dog"},
        "personality": {"title": "Personality", "type": "string", "description": "A dominant personality trait of the dog"}
    },
    "required": ["name", "age", "breed", "personality"],
    "title": "Dog",
    "type": "object"
}

if __name__ == "__main__":
    def testing_this_one(test):
        #  if test == "Running OpenAI Example (MODEL_NON_STREAM)":
        #  if test == "Running Gemini Example (MODEL_STREAM)":
        #  if test == "claude":
        #  if test == "OpenAI Async example":
        #  if test == "OpenAI Example with Attachment":
        #  if test == "Running Gemini Example (MODEL_NON_STREAM) JSON":
        #  if test == "nano MODEL_NON_STREAM Json Response":
        #  if test == "claude MODEL_NON_STREAM Json Response":
        if test == "no":
            return True
        else:
            return False

    # --- OpenAI Example ---
    if testing_this_one("Running OpenAI Example (MODEL_NON_STREAM)"):
        print("\n--- Running OpenAI Example (MODEL_NON_STREAM) ---")
        try:
            runner.run_openai(
                model_name="openai/gpt-4o-mini", # TODO FIXME mentions to "gpt-4o-mini" instead of openai/gpt-4o-mini
                execution_type=LLMExecutionType.MODEL_NON_STREAM,
                prompt=simple_prompt,
                mode="openai_jokes", # just folder to put logs (to use instead of default_mode)
                system="You are a friendly comedian.",
                temperature=0.7,
                max_output_tokens=1200
            )
        except Exception as e:
            print(f"Error running OpenAI: {e}")
    else:
        print("\nSkipping OpenAI example")

    # --- Gemini Example ---
    if testing_this_one("Running Gemini Example (MODEL_STREAM)"):
        print("\n--- Running Gemini Example (MODEL_STREAM) ---")
        try:
            runner.run_gemini(
                system=system_prompt, # system only 
                model_name="gemini-2.5-flash-preview-04-17", # Or "gemini-2.5-pro-preview-03-25"
                execution_type=LLMExecutionType.MODEL_STREAM,
                prompt="What are two key features of the Python language?",
                mode="gemini_python_features",
                temperature=0.8,
                max_output_tokens=1200,
            )
        except Exception as e:
            print(f"Error running Gemini: {e}")
    else:
        print("\nSkipping Gemini example")

    if testing_this_one("Running Gemini Example (MODEL_NON_STREAM) JSON"):
        print("\n--- Running Gemini Example (MODEL_NON_STREAM) JSON ---")
        try:
            full_response_text, llm_response_obj = runner.run_gemini(
                prompt=prompt_for_json_request,
                system=system_prompt_for_json_request,
                model_name="gemini-2.5-pro-preview-03-25",
                execution_type=LLMExecutionType.MODEL_STREAM,
                mode="gemini_json_request",
                #  temperature=0.8, # don't work work with 'json_object=True'
                #  top_p=0.9,
                #  top_k=40,
                #  max_output_tokens=1200, # don't work work with 'json_object=True'
                json_object=True,
                schema=json_schema,
                #  google_search=False,  # Not permited with json_object I guess?
                #  thinking_budget=0, # Not permited with json_object I guess?
                attachments=[],
                    #  application/ogg, application/pdf, audio/aac, audio/aiff,
                    #  audio/flac, audio/mp3, audio/mpeg, audio/ogg, audio/wav,
                    #  image/heic, image/heif, image/jpeg, image/png, image/webp,
                    #  text/csv, text/plain, video/3gpp, video/avi, video/mov, video/mp4,
                    #  video/mpeg, video/mpg, video/quicktime, video/webm, video/wmv,
                    #  video/x-flv
            )
            print(f"▶️"*16, f"> full_response_text: {full_response_text}; ")
            jsonresponse = json.loads(full_response_text)
            print(f"▶️"*16, f"jsonresponse: {jsonresponse}; ")
        except Exception as e:
            print(f"Error running Gemini: {e}")
    else:
        print("\nSkipping Gemini example")

    # --- Claude Example ---
    if testing_this_one("claude"):
        print("\n--- Running Claude Example (MODEL_NON_STREAM) ---")
        claude_model = "claude-3.7-sonnet"
        try:
            runner.run_claude(
                model_name=claude_model,
                execution_type=LLMExecutionType.MODEL_NON_STREAM,
                prompt="Explain black holes in simple terms for a child.",
                mode="claude_science_explain",
                system="You are a patient science educator.",
                temperature=0.6,
                max_tokens=1200
            )
            
            print("\n--- Running Claude Example (MODEL_STREAM with Thinking) ---")
            runner.run_claude(
                model_name=claude_model, # Use a model that supports thinking well
                execution_type=LLMExecutionType.MODEL_STREAM,
                prompt="Outline a plan to build a small community garden. Think step-by-step before you start writing the plan.",
                mode="claude_planning_thinking",
                system="You are a helpful project planner.",
                temperature=1.0, # Often recommended for thinking
                max_tokens=1200,
                thinking=True,
                thinking_budget=1024 
            )
        except Exception as e:
            print(f"Error running Claude: {e}")
    else:
        print("\nSkipping Claude example")

    # --- Async Example (OpenAI ASYNC_MODEL_STREAM) ---
    if testing_this_one("OpenAI Async example"):
        print("\n--- Running OpenAI Async Example (ASYNC_MODEL_STREAM) ---")
        try:
            runner.run_openai(
                model_name="openai/gpt-4o-mini",
                execution_type=LLMExecutionType.ASYNC_MODEL_STREAM,
                prompt="List three common use cases for JSON.",
                mode="openai_async_json_uses",
                max_output_tokens=1200
            )
        except Exception as e:
            print(f"Error running async OpenAI: {e}")
    else:
        print("\nSkipping OpenAI Async example")

    # --- Example with attachments (if model supports it) ---
    # This requires a file named "example_image.jpg" in the same directory
    # or a publicly accessible image URL.
    # Check model.attachment_types for supported types.
    # For example, gpt-4o-mini supports images.
    if testing_this_one("OpenAI Example with Attachment"):
        print("\n--- Running OpenAI Example with Attachment (MODEL_NON_STREAM) ---")
        attachments_list = []
        attachments_list.append(llm.Attachment(path="/home/ph/Downloads/image.jpeg"))
        # You can also use URLs if the model/plugin supports it:
        # attachments_list.append(llm.Attachment.url("https://.../some_image.jpg"))
        try:
            # Ensure the model supports image attachments
            # model_to_check = llm.get_model("gpt-4o-mini")
            # if "image/jpeg" not in model_to_check.attachment_types: # type: ignore
            #    print("gpt-4o-mini (via llm) does not list image/jpeg in attachment_types. Skipping image attachment test.")
            # else:
            runner.run_openai(
                model_name="openai/gpt-4o-mini", 
                execution_type=LLMExecutionType.MODEL_NON_STREAM,
                prompt="Describe this image.",
                mode="openai_image_description",
                attachments=[
                    llm.Attachment(path="/home/ph/Downloads/image.jpeg")
                    #  llm.Attachment(url="https://static.simonwillison.net/static/2024/pelicans.jpg")
                ],
                max_output_tokens=1200
            )
        except Exception as e:
            print(f"Error running OpenAI with attachment: {e}")


    if testing_this_one("nano MODEL_NON_STREAM Json Response"):
        print("\n--- Running OpenAI Example (MODEL_NON_STREAM) ---")
        try:
            full_response_text, llm_response_obj = runner.run_openai(
                prompt=prompt_for_json_request,
                system=system_prompt_for_json_request,
                schema=json_schema,
                model_name="openai/gpt-4o-mini", # TODO FIXME mentions to "gpt-4o-mini" instead of openai/gpt-4o-mini
                execution_type=LLMExecutionType.MODEL_NON_STREAM,
                mode="openai_nano_json", # just folder to put logs (to use instead of default_mode)
                temperature=0.7,
                max_output_tokens=1200,
                store=False, # Whether to store the generated model response for later retrieval via API.
                truncation="auto", # For conversations
                  #  The truncation strategy to use for the model response. If 'auto' and
                  #  the context of this response and previous ones exceeds the model's
                  #  context window size, the model will truncate the response to fit the
                  #  context window by dropping input items in the middle of the
                  #  conversation.
                image_detail="low",
                  #  low = fixed tokens per image.
                  #  high = more tokens for larger images.
                  #  auto = model decides. Default is low.
            )
            print(f"▶️"*16, f"> full_response_text: {full_response_text}; ")
            jsonresponse = json.loads(full_response_text)
            print(f"▶️"*16, f"jsonresponse: {jsonresponse}; ")

        except Exception as e:
            print(f"Error running OpenAI: {e}")
    else:
        print("\nSkipping nano MODEL_NON_STREAM Json Response")

    if testing_this_one("claude MODEL_NON_STREAM Json Response"):
        print("\n--- claude MODEL_NON_STREAM Json Response ---")
        try:
            full_response_text, llm_response_obj = runner.run_claude(
                prompt=prompt_for_json_request,
                system=system_prompt_for_json_request,
                schema=json_schema,
                model_name="claude-3.7-sonnet",
                execution_type=LLMExecutionType.MODEL_NON_STREAM,
                mode="claude_json", # just folder to put logs (to use instead of default_mode)
                temperature=0.7,
                max_tokens=1200,
                thinking=False,
            )
            print(f"▶️"*16, f"> full_response_text: {full_response_text}; ")
            jsonresponse = json.loads(full_response_text)
            print(f"▶️"*16, f"jsonresponse: {jsonresponse}; ")

        except Exception as e:
            print(f"Error running OpenAI: {e}")
    else:
        print("\nSkipping nano MODEL_NON_STREAM Json Response")



    #  OpenAI Chat: gpt-4o-mini-audio-preview
      #  Options:
        #  temperature: float
        #  max_tokens: int
        #  top_p: float
        #  frequency_penalty: float
        #  presence_penalty: float
        #  stop: str
        #  logit_bias: dict, str
        #  seed: int
        #  json_object: boolean
      #  Attachment types:
        #  audio/mpeg, audio/wav
      #  Features:
      #  - streaming
      #  - async


    parser = argparse.ArgumentParser(description="LLM Runner CLI")


                #  model_name="openai/gpt-4o-mini", # TODO FIXME mentions to "gpt-4o-mini" instead of openai/gpt-4o-mini
                #  execution_type=LLMExecutionType.MODEL_NON_STREAM,
                #  prompt=simple_prompt,
                #  mode="openai_jokes", # just folder to put logs (to use instead of default_mode)
                #  system="You are a friendly comedian.",
                #  temperature=0.7,
                #  max_output_tokens=1200
    
    # Required arguments from Bash script
    parser.add_argument("--model_provider", required=True, choices=["openai", "gemini", "claude"], help="The model provider.")
    parser.add_argument("--model_name", required=True, help="The specific model name.")
    parser.add_argument("--execution_type", required=True, choices=[e.name for e in LLMExecutionType], help="The execution type for the LLM.")
    parser.add_argument("--mode", help="Mode for logging purposes.")

    # Optional arguments (common and model-specific)
    parser.add_argument("--system", help="System prompt or instruction.")
    parser.add_argument("--temperature", type=float, help="Sampling temperature.")
    parser.add_argument("--attachments", nargs='+', help="List of attachment file paths.")
    # conversation is not typically passed via CLI like this, skipping for now
    parser.add_argument("--max_output_tokens", type=int, help="Maximum number of tokens in the output (generic).")
    parser.add_argument("--max_tokens", type=int, help="Maximum number of tokens in the output (Claude specific).")
    parser.add_argument("--top_p", type=float, help="Top-p probability mass.")
    parser.add_argument("--schema", type=lambda x: json.loads(x) if x else None, help="JSON schema string for model output.")
    parser.add_argument("--key", help="API key for the LLM service.")

    # Gemini specific
    parser.add_argument("--top_k", type=int, help="Top-k sampling.") # Also used by Claude
    parser.add_argument("--json_object", action="store_true", help="Request JSON object output (Gemini specific).")

    # Claude specific
    parser.add_argument("--thinking", action="store_true", help="Enable thinking mode (Claude specific).")
    parser.add_argument("--thinking_budget", type=int, help="Budget for thinking tokens (Claude specific).")
    parser.add_argument("--prefill", help="Prefill text for the model (Claude specific).")
    parser.add_argument("--hide_prefill", action="store_true", help="Hide prefill text from output (Claude specific).")
    parser.add_argument("--stop_sequences", nargs='+', help="List of stop sequences (Claude specific).")
    
    claude_only_args = [
        "thinking", "thinking_budget", "prefill", "hide_prefill", "stop_sequences"
    ]

    gemini_only_args = [
        "json_object",
    ]

    openai_only_args = [
    ]

    # Use parse_known_args to allow other arbitrary --key value pairs if _run_model supports them via kwargs
    # However, for this implementation, we explicitly define all known args.
    # For any other args passed via named_args in bash that are not defined here, they will cause an error.
    # This is generally safer.
    parsed_args = parser.parse_args()

    prompt_text = sys.stdin.read()
    
    runner = LLMRunner() # Uses default base_folder

    args_dict = vars(parsed_args)

    # Extract core arguments for run_* methods
    model_provider = args_dict.pop('model_provider')
    model_name = args_dict.pop('model_name')
    execution_type_str = args_dict.pop('execution_type')
    mode_for_logging = args_dict.pop('mode')
    print(f"▶️"*16, f"mode_for_logging: {mode_for_logging}")

    if model_provider == "openai":
        # remove claude ones
        for key in claude_only_args:
            args_dict.pop(key)
        # remove gemini ones
        for key in gemini_only_args:
            args_dict.pop(key)
    if model_provider == "claude":
        # remove openai ones
        for key in openai_only_args:
            args_dict.pop(key)
        # remove gemini ones
        for key in gemini_only_args:
            args_dict.pop(key)
        args_dict.pop('mode')
    if model_provider == "gemini":
        # remove openai ones
        for key in openai_only_args:
            args_dict.pop(key)
        # remove claude ones
        for key in claude_only_args:
            args_dict.pop(key)
        args_dict.pop('mode')

    try:
        execution_type_enum = LLMExecutionType[execution_type_str]
    except KeyError:
        valid_types = [e.name for e in LLMExecutionType]
        print(f"Error: Invalid execution_type '{execution_type_str}'. Valid options are: {', '.join(valid_types)}", file=sys.stderr)
        sys.exit(1)

    # Remaining items in args_dict are kwargs for the run methods.
    # Filter out None values, as the run_* methods expect actual values or will use their own defaults.
    run_kwargs = {k: v for k, v in args_dict.items() if v is not None}
    # If a store_true flag is False, it will also be filtered out if v is not None is used.
    # For boolean flags from store_true, args.thinking will be False if not present, True if present.
    # We want to pass False if it's False.
    # Let's adjust run_kwargs population for boolean flags correctly.
    
    # Correctly prepare kwargs, including boolean flags that are False
    processed_run_kwargs = {}
    for k, v in args_dict.items():
        arg_spec = next((action for action in parser._actions if action.dest == k), None)
        if isinstance(arg_spec, argparse._StoreTrueAction): # Handles store_true/store_false
            processed_run_kwargs[k] = v # v will be True or False
        elif v is not None:
            processed_run_kwargs[k] = v
    
    run_kwargs = processed_run_kwargs


    response = None
    try:
        if model_provider == "openai":
            print(f"▶️"*16, f"about to run run_openai ")
            response = runner.run_openai(
                model_name=model_name,
                execution_type=execution_type_enum,
                prompt=prompt_text,
                mode=mode_for_logging,
                **run_kwargs
            )
        elif model_provider == "gemini":
            response = runner.run_gemini(
                model_name=model_name,
                execution_type=execution_type_enum,
                prompt=prompt_text,
                mode=mode_for_logging,
                **run_kwargs
            )
        elif model_provider == "claude":
            # run_claude itself handles max_output_tokens vs max_tokens logic
            response = runner.run_claude(
                model_name=model_name,
                execution_type=execution_type_enum,
                prompt=prompt_text,
                mode=mode_for_logging,
                **run_kwargs
            )
        else:
            # This case should ideally not be reached if choices are enforced by argparse for model_provider
            print(f"Error: Unknown model_provider '{model_provider}'", file=sys.stderr)
            sys.exit(1)

        if response:
            # _run_model for non-streaming returns response.text which is a string
            # For streaming, it yields chunks. This script assumes non-streaming based on MODEL_NON_STREAM.
            print(response)
            print(f"▶️"*16, f"final response: {response}; ")

    except Exception as e:
        print(f"An error occurred during LLM execution: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc() # For more detailed debugging
        sys.exit(1)
