"""
LaTeX Snippets System - Provides reusable LaTeX macros and components
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

SNIPPETS_DIR = Path(__file__).parent / "snippets"

def load_snippet(name: str) -> Dict[str, Any]:
    """Load a snippet definition from JSON file"""
    snippet_file = SNIPPETS_DIR / f"{name}.json"
    if not snippet_file.exists():
        raise FileNotFoundError(f"Snippet '{name}' not found")
    
    with open(snippet_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_available_snippets() -> List[Dict[str, str]]:
    """List all available snippets with their descriptions"""
    snippets = []
    for snippet_file in SNIPPETS_DIR.glob("*.json"):
        try:
            snippet = load_snippet(snippet_file.stem)
            snippets.append({
                "name": snippet["name"],
                "description": snippet["description"],
                "parameters": len(snippet.get("parameters", []))
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return snippets

def get_snippet_info(name: str) -> Dict[str, Any]:
    """Get detailed information about a snippet including parameters"""
    snippet = load_snippet(name)
    return {
        "name": snippet["name"],
        "description": snippet["description"],
        "parameters": snippet.get("parameters", []),
        "template": snippet["template"]
    }

def render_snippet(name: str, **kwargs) -> str:
    """Render a snippet with the provided parameters"""
    snippet = load_snippet(name)
    template = snippet["template"]
    
    # Simple template rendering - replace {param} with values
    for param in snippet.get("parameters", []):
        param_name = param["name"]
        param_value = kwargs.get(param_name, param.get("default", ""))
        
        # Handle required parameters
        if param.get("required", False) and not param_value:
            raise ValueError(f"Required parameter '{param_name}' not provided")
        
        # Replace placeholder
        template = template.replace(f"{{{param_name}}}", str(param_value))
    
    # Handle simple conditionals: {{#if param}}content{{/if}}
    template = _handle_conditionals(template, kwargs)
    
    return template

def _handle_conditionals(template: str, params: Dict[str, Any]) -> str:
    """Handle simple {{#if param}}content{{/if}} conditionals"""
    # Pattern to match {{#if param}}content{{/if}}
    pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
    
    def replace_conditional(match):
        param_name = match.group(1)
        content = match.group(2)
        param_value = params.get(param_name, "")
        
        # Return content if parameter has a truthy value, empty string otherwise
        return content if param_value else ""
    
    return re.sub(pattern, replace_conditional, template, flags=re.DOTALL)