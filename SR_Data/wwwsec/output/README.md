# Queue Directory

This directory contains the queue file (`queue.txt`) used for requesting visualizations from the SR_Data system.

## Usage

The `queue.txt` file is monitored by the system when running in MERC_FIN_AUTO_ROBO mode.
Write visualization requests to this file in the format: `<type> <indicator>`.

Example:
```
1 IPCA    # Request IPCA visualization
2 PIB     # Request GDP visualization
3 SELIC   # Request SELIC rate visualization
```

## File Structure

- `queue.txt`: The main queue file for visualization requests
- Default format: "0 0" when no request is pending
- System automatically clears the file after processing each request

## Permissions

Ensure that both the directory and queue.txt file have appropriate read/write permissions for the system to function properly.
