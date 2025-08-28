# Learning Prompt 12: CI/CD Pipelines and Automation

## Objective
Master continuous integration and continuous deployment (CI/CD) pipelines, automated testing, deployment strategies, and DevOps practices for Python applications.

## Prerequisites
Complete prompts #1-11 to understand the codebase, testing, configuration, and package management.

## Your Task
Design and implement a comprehensive CI/CD pipeline for the py-simple project, covering automated testing, code quality checks, security scanning, and deployment strategies.

## Prompt to Use with AI Assistant

```
Create a comprehensive CI/CD pipeline and deployment strategy for the py_simple project. Cover:

1. **CI/CD Pipeline Architecture**
   - Design a complete GitHub Actions workflow for the project
   - Implement multi-stage pipeline with parallel and sequential jobs
   - Create environment-specific deployment pipelines
   - Set up matrix testing for multiple Python versions and platforms
   - Implement proper artifact handling and caching strategies

2. **Automated Testing and Quality Gates**
   - Implement comprehensive test automation (unit, integration, e2e)
   - Set up code coverage reporting and quality gates
   - Add linting, formatting, and type checking automation
   - Implement security scanning (SAST, dependency vulnerabilities)
   - Create performance benchmarking and regression testing

3. **Build and Release Management**
   - Automate package building and distribution
   - Implement semantic versioning and automated releases
   - Create release notes generation and changelog management
   - Set up multi-platform builds and compatibility testing
   - Implement rollback and hotfix deployment strategies

4. **Deployment Strategies**
   - Design deployment to multiple environments (dev, staging, prod)
   - Implement blue-green and canary deployment patterns
   - Create infrastructure as code (IaC) templates
   - Set up automated environment provisioning and teardown
   - Implement deployment approval workflows and gates

5. **Monitoring and Observability**
   - Set up deployment monitoring and health checks
   - Implement automated rollback on deployment failures
   - Create alerting and notification systems
   - Add deployment metrics and success rate tracking
   - Set up log aggregation and error tracking

6. **Security and Compliance**
   - Implement secrets management in CI/CD
   - Add security scanning and compliance checks
   - Create secure artifact signing and verification
   - Implement access controls and audit logging
   - Add vulnerability management and remediation workflows

Create your comprehensive CI/CD guide in:
docs/learning/$(date +%Y%m%d%H%M)-cicd-pipeline-guide.md

Include:
- Complete GitHub Actions workflow files
- Deployment scripts and infrastructure templates
- Monitoring and alerting configuration
- Security and compliance procedures
- Troubleshooting and maintenance guides
```

## Key Learning Points
After completing this exercise, you should understand:
- CI/CD pipeline design principles and best practices
- Automated testing and quality gate implementation
- Deployment strategies and environment management
- Infrastructure as Code (IaC) concepts and tools
- Security considerations in CI/CD pipelines
- Monitoring and observability for deployments
- Release management and version control strategies

## CI/CD Pipeline Architecture

### 1. Complete GitHub Actions Workflow
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"
  UV_VERSION: "latest"

jobs:
  # Job 1: Code Quality and Testing
  test:
    name: Test and Quality Checks
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better caching

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      - name: Cache UV dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/uv
          key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}
          restore-keys: |
            ${{ runner.os }}-uv-

      - name: Install dependencies
        run: |
          uv venv .venv
          uv pip install -e ".[dev,test]"

      - name: Run linting
        run: |
          uv run ruff check .
          uv run ruff format --check .

      - name: Run type checking
        run: uv run mypy py_simple/

      - name: Run tests with coverage
        run: |
          uv run pytest \
            --cov=py_simple \
            --cov-report=xml \
            --cov-report=term-missing \
            --junitxml=test-results.xml

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-${{ matrix.os }}-py${{ matrix.python-version }}

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results-${{ matrix.os }}-py${{ matrix.python-version }}
          path: test-results.xml

  # Job 2: Security Scanning
  security:
    name: Security Scanning
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install safety bandit pip-audit

      - name: Run safety check
        run: safety check --json --output safety-report.json
        continue-on-error: true

      - name: Run bandit security scan
        run: bandit -r py_simple/ -f json -o bandit-report.json
        continue-on-error: true

      - name: Run pip-audit
        run: pip-audit --format=json --output=audit-report.json
        continue-on-error: true

      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            safety-report.json
            bandit-report.json
            audit-report.json

  # Job 3: Build Package
  build:
    name: Build Package
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.event_name == 'push' || github.event_name == 'release'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install build dependencies
        run: pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  # Job 4: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/

      - name: Deploy to staging environment
        run: |
          # Deploy to staging server or cloud environment
          echo "Deploying to staging..."
          # Add actual deployment commands here

      - name: Run smoke tests
        run: |
          # Run basic smoke tests against staging
          echo "Running smoke tests..."

  # Job 5: Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, deploy-staging]
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/

      - name: Deploy to production
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install twine
          twine upload dist/*

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false

  # Job 6: Performance Testing
  performance:
    name: Performance Testing
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev,test]"
          pip install pytest-benchmark

      - name: Run performance tests
        run: pytest tests/performance/ --benchmark-json=benchmark.json

      - name: Upload benchmark results
        uses: actions/upload-artifact@v3
        with:
          name: benchmark-results
          path: benchmark.json
```

### 2. Environment-Specific Workflows
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Deploy to staging
        run: |
          # AWS deployment example
          aws lambda update-function-code \
            --function-name py-simple-staging \
            --image-uri $ECR_REGISTRY/py-simple:$GITHUB_SHA

      - name: Wait for deployment
        run: |
          aws lambda wait function-updated \
            --function-name py-simple-staging

      - name: Run health checks
        run: |
          curl -f https://staging-api.company.com/health || exit 1

      - name: Notify deployment status
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#deployments'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Advanced Deployment Strategies

### 1. Blue-Green Deployment Script
```python
#!/usr/bin/env python3
"""Blue-Green deployment script."""

import subprocess
import time
import requests
import sys
from typing import Dict, Any

class BlueGreenDeployer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_env = self._get_current_environment()
        self.target_env = 'green' if self.current_env == 'blue' else 'blue'
    
    def deploy(self):
        """Execute blue-green deployment."""
        print(f"Starting blue-green deployment...")
        print(f"Current environment: {self.current_env}")
        print(f"Target environment: {self.target_env}")
        
        try:
            # Step 1: Deploy to target environment
            self._deploy_to_environment(self.target_env)
            
            # Step 2: Wait for deployment to be ready
            self._wait_for_health_check(self.target_env)
            
            # Step 3: Run smoke tests
            self._run_smoke_tests(self.target_env)
            
            # Step 4: Switch traffic
            self._switch_traffic(self.target_env)
            
            # Step 5: Verify production traffic
            self._verify_production_health()
            
            # Step 6: Clean up old environment
            self._cleanup_old_environment(self.current_env)
            
            print(f"Deployment successful! Traffic switched to {self.target_env}")
            
        except Exception as e:
            print(f"Deployment failed: {e}")
            self._rollback()
            sys.exit(1)
    
    def _deploy_to_environment(self, env: str):
        """Deploy application to specified environment."""
        print(f"Deploying to {env} environment...")
        # AWS ECS example
        subprocess.run([
            'aws', 'ecs', 'update-service',
            '--cluster', f'py-simple-{env}',
            '--service', f'py-simple-service-{env}',
            '--task-definition', f'py-simple:{self.config["version"]}'
        ], check=True)
    
    def _wait_for_health_check(self, env: str):
        """Wait for environment to be healthy."""
        url = f"https://{env}.py-simple.company.com/health"
        max_attempts = 30
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"{env} environment is healthy")
                    return
            except Exception as e:
                print(f"Health check attempt {attempt + 1} failed: {e}")
            
            time.sleep(10)
        
        raise Exception(f"Health check failed for {env} after {max_attempts} attempts")
    
    def _switch_traffic(self, env: str):
        """Switch load balancer traffic to new environment."""
        print(f"Switching traffic to {env}...")
        # AWS ALB target group example
        subprocess.run([
            'aws', 'elbv2', 'modify-listener',
            '--listener-arn', self.config['listener_arn'],
            '--default-actions', f'Type=forward,TargetGroupArn={self.config[f"{env}_target_group"]}'
        ], check=True)
```

### 2. Canary Deployment with Gradual Rollout
```python
class CanaryDeployer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.traffic_stages = [5, 25, 50, 100]  # Gradual traffic increase
    
    def deploy(self):
        """Execute canary deployment with gradual traffic increase."""
        try:
            # Deploy canary version
            self._deploy_canary()
            
            # Gradually increase traffic
            for traffic_percentage in self.traffic_stages:
                print(f"Increasing canary traffic to {traffic_percentage}%")
                self._update_traffic_split(traffic_percentage)
                
                # Monitor metrics for 5 minutes at each stage
                if not self._monitor_metrics(duration=300):
                    raise Exception(f"Metrics degraded at {traffic_percentage}% traffic")
                
                if traffic_percentage < 100:
                    time.sleep(60)  # Wait between stages
            
            # Clean up old version
            self._promote_canary()
            print("Canary deployment successful!")
            
        except Exception as e:
            print(f"Canary deployment failed: {e}")
            self._rollback_canary()
            sys.exit(1)
    
    def _monitor_metrics(self, duration: int) -> bool:
        """Monitor key metrics during canary deployment."""
        metrics_to_check = [
            'error_rate',
            'response_time_p95',
            'throughput'
        ]
        
        for _ in range(duration // 30):  # Check every 30 seconds
            current_metrics = self._get_current_metrics()
            baseline_metrics = self._get_baseline_metrics()
            
            for metric in metrics_to_check:
                if not self._is_metric_acceptable(
                    current_metrics[metric],
                    baseline_metrics[metric],
                    metric
                ):
                    return False
            
            time.sleep(30)
        
        return True
```

## Infrastructure as Code

### 1. Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim as builder

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -e .

# Production stage
FROM python:3.11-slim as production

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Copy application code
COPY --chown=appuser:appuser py_simple/ /app/py_simple/
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import py_simple.main; print('OK')" || exit 1

# Run application
CMD ["python", "-m", "py_simple.main"]
```

### 2. Kubernetes Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py-simple
  labels:
    app: py-simple
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: py-simple
  template:
    metadata:
      labels:
        app: py-simple
    spec:
      containers:
      - name: py-simple
        image: py-simple:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: py-simple-service
spec:
  selector:
    app: py-simple
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

### 3. Terraform Infrastructure
```hcl
# terraform/main.tf
provider "aws" {
  region = var.aws_region
}

# ECS Cluster
resource "aws_ecs_cluster" "py_simple" {
  name = "py-simple-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "py_simple" {
  family                   = "py-simple"
  network_mode            = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                     = "256"
  memory                  = "512"
  execution_role_arn      = aws_iam_role.ecs_execution_role.arn
  task_role_arn          = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "py-simple"
      image = "${aws_ecr_repository.py_simple.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8080
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.py_simple.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "py_simple" {
  name            = "py-simple-service"
  cluster         = aws_ecs_cluster.py_simple.id
  task_definition = aws_ecs_task_definition.py_simple.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.py_simple.arn
    container_name   = "py-simple"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.py_simple]
}
```

## Monitoring and Observability

### 1. Application Performance Monitoring
```python
# monitoring/apm.py
import time
from functools import wraps
from typing import Dict, Any
import psutil
import logging

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.logger = logging.getLogger(__name__)
    
    def track_performance(self, func):
        """Decorator to track function performance."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            except Exception as e:
                success = False
                raise
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                
                metrics = {
                    'function': func.__name__,
                    'duration': end_time - start_time,
                    'memory_delta': end_memory - start_memory,
                    'success': success,
                    'timestamp': time.time()
                }
                
                self._record_metrics(metrics)
        
        return wrapper
    
    def _record_metrics(self, metrics: Dict[str, Any]):
        """Record metrics for monitoring."""
        # Send to monitoring system (CloudWatch, DataDog, etc.)
        self.logger.info(f"Performance metrics: {metrics}")
```

### 2. Health Check Implementation
```python
# health.py
from typing import Dict, Any
import requests
import psutil
from pathlib import Path

class HealthChecker:
    def __init__(self, config):
        self.config = config
    
    def get_health_status(self) -> Dict[str, Any]:
        """Comprehensive health check."""
        health = {
            'status': 'healthy',
            'timestamp': time.time(),
            'checks': {}
        }
        
        # Database connectivity
        health['checks']['database'] = self._check_database()
        
        # External API connectivity
        health['checks']['api'] = self._check_external_api()
        
        # File system health
        health['checks']['filesystem'] = self._check_filesystem()
        
        # Memory usage
        health['checks']['memory'] = self._check_memory()
        
        # Determine overall status
        if any(check['status'] == 'unhealthy' for check in health['checks'].values()):
            health['status'] = 'unhealthy'
        elif any(check['status'] == 'degraded' for check in health['checks'].values()):
            health['status'] = 'degraded'
        
        return health
    
    def _check_external_api(self) -> Dict[str, Any]:
        """Check external API connectivity."""
        try:
            response = requests.get(
                self.config.api_url,
                timeout=5,
                headers={'User-Agent': 'py-simple-health-check'}
            )
            
            return {
                'status': 'healthy' if response.status_code == 200 else 'degraded',
                'response_time': response.elapsed.total_seconds(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
```

## Follow-up Questions
1. How would you implement automated rollback based on metrics?
2. What metrics are most important to monitor during deployments?
3. How would you handle database migrations in a CI/CD pipeline?
4. What's the difference between blue-green and canary deployments?
5. How would you implement feature flags in your deployment strategy?

## CI/CD Best Practices
1. **Fast Feedback**: Keep pipeline execution time under 10 minutes
2. **Fail Fast**: Run quick checks before expensive operations
3. **Parallel Execution**: Run independent jobs in parallel
4. **Artifact Management**: Store and version build artifacts
5. **Security First**: Scan for vulnerabilities early and often
6. **Infrastructure as Code**: Version control infrastructure changes
7. **Monitoring**: Monitor deployments and rollback automatically on issues

## Advanced CI/CD Patterns
1. **GitOps**: Use Git as source of truth for deployments
2. **Progressive Delivery**: Gradual feature rollout with monitoring
3. **Chaos Engineering**: Test system resilience in CI/CD
4. **Contract Testing**: Ensure API compatibility across services
5. **Multi-Cloud**: Deploy to multiple cloud providers for resilience

This completes the comprehensive set of learning prompts for your friend! The progression takes them from basic code understanding to advanced DevOps practices.