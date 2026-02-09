---
name: mcp-auth
description: Implements OAuth 2.1 authorization for Model Context Protocol (MCP) servers using Scalekit. Use when building or securing MCP servers, adding authentication to AI tools, or when user mentions "MCP auth", "OAuth for MCP", "secure MCP server", "Scalekit MCP integration", or "protect MCP tools".
license: MIT
metadata:
  author: Scalekit
  version: 1.0.0
  category: security
  tags: [oauth, mcp, authentication, scalekit, authorization]
  documentation: https://docs.scalekit.com/authenticate/mcp
---

# MCP OAuth 2.1 Authorization

Production-ready OAuth 2.1 authorization for Model Context Protocol (MCP) servers using Scalekit. Secures MCP servers so only authenticated and authorized users can access tools through AI hosts like Claude Desktop, Cursor, or VS Code.

## Quick Start

### Step 1: Setup Scalekit SDK

Install the SDK for your language:

**Node.js:**
```bash
npm install @scalekit-sdk/node
```

**Python:**
```bash
pip install scalekit-sdk-python
```

Initialize client with credentials from [Scalekit Dashboard](https://app.scalekit.com):
- Environment URL
- Client ID
- Client Secret

### Step 2: Register MCP Server

In Scalekit Dashboard > MCP servers > Add MCP server:

1. **Name**: Identify your MCP server easily
2. **Enable Dynamic Client Registration (DCR)**: Auto-register MCP hosts
3. **Enable Client ID Metadata Document (CIMD)**: Auto-fetch client metadata
4. **Server URL** (optional): Your server's unique identifier (e.g., `https://mcp.yourapp.com`)
5. **Access token lifetime**: 300-3600 seconds recommended
6. **Scopes**: Define permissions (e.g., `todo:read`, `todo:write`)

**IMPORTANT**: Restart your MCP server after toggling DCR or CIMD settings.

### Step 3: Implement Discovery Endpoint

Create `.well-known/oauth-protected-resource` endpoint with metadata from Dashboard > MCP Servers > Your server > Metadata JSON.

**Node.js (Express):**
```javascript
app.get('/.well-known/oauth-protected-resource', (req, res) => {
  res.json({
    "authorization_servers": [
      "https://<SCALEKIT_ENVIRONMENT_URL>/resources/<YOUR_RESOURCE_ID>"
    ],
    "bearer_methods_supported": ["header"],
    "resource": "https://mcp.yourapp.com",
    "resource_documentation": "https://mcp.yourapp.com/docs",
    "scopes_supported": ["todo:read", "todo:write"]
  });
});
```

**Python (FastAPI):**
```python
@app.get("/.well-known/oauth-protected-resource")
async def get_oauth_protected_resource():
    return JSONResponse({
        "authorization_servers": [
            "https://<SCALEKIT_ENVIRONMENT_URL>/resources/<YOUR_RESOURCE_ID>"
        ],
        "bearer_methods_supported": ["header"],
        "resource": "https://mcp.yourapp.com",
        "resource_documentation": "https://mcp.yourapp.com/docs",
        "scopes_supported": ["todo:read", "todo:write"]
    })
```

### Step 4: Implement Token Validation Middleware

**Node.js:**
```javascript
import { Scalekit } from '@scalekit-sdk/node';

const scalekit = new Scalekit(
  process.env.SCALEKIT_ENVIRONMENT_URL,
  process.env.SCALEKIT_CLIENT_ID,
  process.env.SCALEKIT_CLIENT_SECRET
);

const RESOURCE_ID = 'https://your-mcp-server.com';
const METADATA_ENDPOINT = 'https://your-mcp-server.com/.well-known/oauth-protected-resource';

export async function authMiddleware(req, res, next) {
  try {
    // Allow public access to well-known endpoints
    if (req.path.includes('.well-known')) {
      return next();
    }

    // Extract Bearer token
    const authHeader = req.headers['authorization'];
    const token = authHeader?.startsWith('Bearer ')
      ? authHeader.split('Bearer ')[1]?.trim()
      : null;

    if (!token) {
      throw new Error('Missing or invalid Bearer token');
    }

    // Validate token
    await scalekit.validateToken(token, {
      audience: [RESOURCE_ID]
    });

    next();
  } catch (err) {
    return res
      .status(401)
      .set('WWW-Authenticate', `Bearer realm="OAuth", resource_metadata="${METADATA_ENDPOINT}"`)
      .end();
  }
}

app.use('/', authMiddleware);
```

**Python:**
```python
from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions
from fastapi import Request, HTTPException, status

scalekit_client = ScalekitClient(
    env_url=os.getenv("SCALEKIT_ENVIRONMENT_URL"),
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET")
)

RESOURCE_ID = "https://your-mcp-server.com"
METADATA_ENDPOINT = "https://your-mcp-server.com/.well-known/oauth-protected-resource"

async def auth_middleware(request: Request, call_next):
    # Allow public access to well-known endpoints
    if request.url.path.startswith("/.well-known"):
        return await call_next(request)

    # Extract Bearer token
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1].strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="{METADATA_ENDPOINT}"'}
        )

    # Validate token
    try:
        options = TokenValidationOptions(
            issuer=os.getenv("SCALEKIT_ENVIRONMENT_URL"),
            audience=[RESOURCE_ID]
        )
        scalekit_client.validate_token(token, options=options)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="{METADATA_ENDPOINT}"'}
        )

    return await call_next(request)

app.middleware("http")(auth_middleware)
```

## Advanced Features

### Scope-Based Authorization (Optional)

Add fine-grained access control at the tool execution level:

**Node.js:**
```javascript
try {
    await scalekit.validateToken(token, {
      audience: [RESOURCE_ID],
      requiredScopes: [scope]
    });
} catch(error) {
    return res.status(403).json({
        error: 'insufficient_scope',
        error_description: `Required scope: ${scope}`,
        scope: scope
    });
}
```

**Python:**
```python
try:
    scalekit_client.validate_token(
        token,
        options=TokenValidationOptions(
            audience=[RESOURCE_ID],
            required_scopes=[scope]
        )
    )
except ScalekitValidateTokenFailureException:
    return {
        "error": "insufficient_scope",
        "error_description": f"Required scope: {scope}",
        "scope": scope
    }
```

### Additional Authentication Methods

Enable without changing your MCP server implementation:

- **Enterprise SSO**: Organizations authenticate through identity providers (Okta, Azure AD, Google Workspace)
- **Social Logins**: Users authenticate via Google, GitHub, Microsoft
- **Custom Auth**: Use your own authentication system

See [Scalekit documentation](https://docs.scalekit.com/mcp/auth-methods) for setup instructions.

## Key Configuration Values

Replace these placeholders with actual values from your Scalekit Dashboard:

| Placeholder | Where to Find | Example |
|------------|---------------|---------|
| `<SCALEKIT_ENVIRONMENT_URL>` | Dashboard > Settings | `https://yourenv.scalekit.com` |
| `<YOUR_RESOURCE_ID>` | Dashboard > MCP Servers > Your Server | `res_123456789` or custom URL |
| `SCALEKIT_CLIENT_ID` | Dashboard > API Keys | Environment variable |
| `SCALEKIT_CLIENT_SECRET` | Dashboard > API Keys | Environment variable |

**For FastMCP users**: Use base URL with trailing slash (e.g., `https://mcp.example.com/`)

## Workflow Checklist

When implementing OAuth for an MCP server, follow this sequence:

```
Implementation Progress:
- [ ] Step 1: Install Scalekit SDK
- [ ] Step 2: Create MCP server in Scalekit Dashboard
- [ ] Step 3: Implement discovery endpoint (.well-known/oauth-protected-resource)
- [ ] Step 4: Add token validation middleware
- [ ] Step 5: Test with MCP client (Claude, Cursor, VS Code)
- [ ] Step 6: (Optional) Add scope-based authorization
- [ ] Step 7: Configure additional auth methods if needed
```

## Common Issues

### Issue: Token validation fails
**Cause**: Incorrect RESOURCE_ID or audience mismatch
**Solution**:
- Verify RESOURCE_ID matches Server URL in Scalekit Dashboard
- If no Server URL set, use autogenerated resource ID (e.g., `res_123456789`)
- Check token `aud` claim matches expected audience

### Issue: Discovery endpoint not found
**Cause**: Endpoint not properly implemented or path incorrect
**Solution**:
- Confirm endpoint path is exactly `/.well-known/oauth-protected-resource`
- Test with: `curl https://your-server.com/.well-known/oauth-protected-resource`
- Verify endpoint returns JSON with `authorization_servers` field

### Issue: MCP client can't connect
**Cause**: DCR or CIMD configuration issue
**Solution**:
- Restart MCP server after toggling DCR/CIMD in Dashboard
- Enable both DCR and CIMD for public MCP clients (Claude, Cursor, VS Code)
- Check MCP client supports CIMD (falls back to DCR if not)

### Issue: Middleware blocks all requests
**Cause**: Well-known endpoint not exempted from auth
**Solution**:
- Ensure middleware skips `.well-known` paths before token validation
- Check middleware ordering - auth middleware should come after route definitions for public endpoints

## Production Deployment Checklist

Before deploying to production:

- [ ] Configure proper CORS policies for MCP server endpoints
- [ ] Set up monitoring and logging for authorization events
- [ ] Use HTTPS for all communications
- [ ] Store client secrets securely using environment variables or secret management
- [ ] Configure appropriate token lifetimes (300-3600 seconds recommended)
- [ ] Test with various AI hosts (Claude Desktop, Cursor, VS Code)
- [ ] Document authentication flow for end users
- [ ] Set up error monitoring for failed auth attempts

## Example Use Cases

**Sales team member using Claude Desktop:**
```
User: "Show me customer information for Acme Corp"
→ MCP server validates token
→ Checks user has 'customer:read' scope
→ Returns customer data
```

**Developer using VS Code/Cursor:**
```
User: "Create a new GitHub issue for the bug we discussed"
→ MCP server validates token
→ Verifies 'issues:write' scope
→ Creates issue via GitHub MCP server
```

## Resources

- [Sample MCP server with auth](https://github.com/scalekit-inc/mcp-auth-demos)
- [Scalekit MCP Documentation](https://docs.scalekit.com/authenticate/mcp)
- [FastMCP Integration Guide](https://docs.scalekit.com/authenticate/mcp/fastmcp-quickstart)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
