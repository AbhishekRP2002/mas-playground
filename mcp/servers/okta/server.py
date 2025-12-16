"""Main MCP server implementation for Okta using FastMCP 2.8.1."""

import os
import logging
from fastmcp import FastMCP

logger = logging.getLogger("okta_mcp")


def create_server(enable_auth: bool = False):
    """Create and configure the Okta MCP server using FastMCP 2.8.1."""
    try:
        # Create server with modern FastMCP features
        mcp = FastMCP(
            name="Okta MCP Server",
            instructions="""
            This server provides Okta Identity Cloud management capabilities.
            Use list_okta_users() to search and filter users with SCIM expressions.
            Use get_okta_user() to retrieve detailed user information.
            All operations require proper Okta API credentials in environment variables.
            """,
            mask_error_details=False,  # Show detailed errors for debugging
        )

        # Create Okta client wrapper (will initialize on demand)
        from mcp.servers.okta.utils.okta_client import OktaMcpClient

        okta_client = OktaMcpClient()  # No immediate initialization

        # Register tools with the lazy client
        logger.info("Registering Okta tools")
        from mcp.servers.okta.tools.user_tools import register_user_tools
        from mcp.servers.okta.tools.apps_tools import register_apps_tools
        from mcp.servers.okta.tools.log_events_tools import register_log_events_tools
        from mcp.servers.okta.tools.group_tools import register_group_tools
        from mcp.servers.okta.tools.policy_network_tools import register_policy_tools
        from mcp.servers.okta.tools.datetime_tools import register_datetime_tools
        from mcp.servers.okta.tools.special_tools.access_analysis_tools import (
            register_access_analysis_tools,
        )
        from mcp.servers.okta.tools.special_tools.suspicious_report_analysis import (
            register_login_risk_analysis_tools,
        )

        register_user_tools(mcp, okta_client)
        register_apps_tools(mcp, okta_client)
        register_log_events_tools(mcp, okta_client)
        register_group_tools(mcp, okta_client)
        register_policy_tools(mcp, okta_client)
        register_datetime_tools(mcp, okta_client)
        register_access_analysis_tools(mcp, okta_client)
        register_login_risk_analysis_tools(mcp, okta_client)

        logger.info("Okta MCP server created successfully with all tools registered")

        return mcp

    except Exception as e:
        logger.error(f"Error creating Okta MCP server: {e}")
        raise


def run_with_stdio(server):
    """Run the server with STDIO transport (secure, default)."""
    logger.info("Starting Okta server with STDIO transport")
    server.run()  # FastMCP defaults to STDIO


def run_with_http(server, host="0.0.0.0", port=3000):
    """Run the server with HTTP transport (modern, recommended for web)."""
    logger.info(f"Starting Okta server with HTTP transport on {host}:{port}")

    try:
        server.run(transport="streamable-http", host=host, port=port)
    except TypeError as e:
        logger.warning(f"Host/port not supported in this FastMCP version: {e}")
        server.run(transport="streamable-http")


def run_with_sse(server, host="0.0.0.0", port=3000):
    """Run the server with SSE transport (deprecated)."""
    logger.warning("SSE transport is deprecated in FastMCP, use --http instead")
    logger.info(f"Starting Okta server with SSE transport on {host}:{port}")

    try:
        server.run(transport="sse", host=host, port=port)
    except (ValueError, TypeError) as e:
        logger.warning(f"SSE transport failed ({e}), falling back to HTTP")
        run_with_http(server, host, port)


if __name__ == "__main__":
    server = create_server()
    run_with_stdio(server)
