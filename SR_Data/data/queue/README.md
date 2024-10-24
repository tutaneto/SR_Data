# Queue System Directory

This directory contains the queue system for SR_Data visualization requests.

## Structure

- `queue.txt`: Active queue file containing pending visualization requests
- `processed/`: Directory containing processed queue files for record-keeping
- `failed/`: Directory containing failed queue entries for debugging

## Queue File Format

Each line in the queue file should follow this format:
```
<request_type> <parameters>
```

Example:
```
1 IPCA
2 PIB
```

## Usage

The main program monitors the `queue.txt` file for new visualization requests. Once processed, the queue entries are moved to either the `processed/` or `failed/` directory depending on the outcome.

For more details on request types and parameters, see the main documentation.
