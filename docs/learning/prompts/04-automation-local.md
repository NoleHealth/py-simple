# Learning Prompt 4: Local Automation - Cron, Systemd, and Task Scheduling

## Objective
Learn how to automate Python scripts locally using various scheduling mechanisms, understand their trade-offs, and implement robust automation solutions.

## Prerequisites
Complete prompts #1-3 to understand the codebase and CLI implementation.

## Your Task
Explore different methods for automating the py-simple script locally, including cron jobs, systemd services, and other scheduling options. Learn when to use each approach.

## Prompt to Use with AI Assistant

```
Create a comprehensive guide for automating the py_simple script using local scheduling mechanisms. Cover:

1. **Cron Job Implementation**
   - Create cron job configurations for different schedules (hourly, daily, weekly)
   - Handle environment variables and PATH issues in cron
   - Implement proper logging for cron jobs
   - Add error handling and notification for failed runs
   - Show how to pass command-line parameters via cron

2. **Systemd Service & Timer**
   - Create a systemd service file for the py_simple script
   - Create systemd timer for scheduled execution
   - Configure proper logging through journald
   - Handle service dependencies and error recovery
   - Show how to manage the service (start, stop, status, logs)

3. **Python-based Task Scheduling**
   - Implement scheduling using the `schedule` library
   - Create a daemon version that runs continuously
   - Add graceful shutdown handling
   - Implement retry logic and error recovery
   - Compare with external scheduling solutions

4. **Monitoring & Maintenance**
   - Log rotation and management
   - Health checks and monitoring
   - Notification systems for failures
   - Performance monitoring and resource usage
   - Backup and recovery procedures for output data

5. **Security & Best Practices**
   - Running with minimal privileges
   - Secure handling of credentials and environment variables
   - File permissions and security considerations
   - Isolation and containerization options

Create your automation guide in:
docs/learning/$(date +%Y%m%d%H%M)-local-automation-guide.md

Include:
- Complete configuration files (cron, systemd, etc.)
- Step-by-step setup instructions
- Troubleshooting guide for common issues
- Comparison table of different approaches
- Security checklist and best practices
```

## Key Learning Points
After completing this exercise, you should understand:
- Different local automation mechanisms and their use cases
- Environment and PATH considerations for automated scripts
- Logging and monitoring strategies for automated processes
- Error handling and recovery in automated systems
- Security considerations for running automated scripts
- Resource management and system integration

## Automation Methods to Explore

### 1. Cron Jobs
- **Best for**: Simple time-based scheduling
- **Pros**: Built into most Unix systems, simple syntax
- **Cons**: Limited error handling, environment issues
- **Use cases**: Daily/weekly data processing, cleanup tasks

### 2. Systemd Services/Timers
- **Best for**: Complex services with dependencies
- **Pros**: Better logging, error handling, service management
- **Cons**: Linux-specific, more complex setup
- **Use cases**: Production services, system integration

### 3. Python Scheduling Libraries
- **Best for**: Complex scheduling logic within Python
- **Pros**: Full Python control, flexible scheduling
- **Cons**: Always-running process, more resource usage
- **Use cases**: Dynamic scheduling, complex business logic

### 4. Task Queue Systems
- **Best for**: High-volume, distributed processing
- **Pros**: Scalability, reliability, monitoring
- **Cons**: Additional infrastructure, complexity
- **Use cases**: Production systems, microservices

## Common Automation Challenges
1. **Environment Variables** - Scripts need proper environment setup
2. **Working Directory** - Scripts may rely on specific paths
3. **Logging** - Output needs to be captured and managed
4. **Error Handling** - Failures need to be detected and handled
5. **Resource Management** - Memory and CPU usage monitoring
6. **Security** - Proper permissions and credential management

## Follow-up Questions
1. What happens if the script takes longer to run than the scheduled interval?
2. How would you handle API rate limits in automated runs?
3. What's the best way to notify administrators of failures?
4. How would you prevent multiple instances from running simultaneously?
5. What logs should be kept and for how long?

## Testing Your Automation
1. **Simulate Failures** - Test how your automation handles API outages
2. **Resource Limits** - Test behavior under low memory/disk space
3. **Long Running Tasks** - Test scheduling conflicts
4. **Permission Issues** - Test with restricted user accounts
5. **Recovery Testing** - Test restart and recovery procedures

## Next Steps
After mastering local automation, you'll explore cloud-based automation options in prompt #5.