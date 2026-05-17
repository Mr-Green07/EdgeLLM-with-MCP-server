// Jenkins Pipeline Configuration for Voice Assistant ASR
// This file contains shared pipeline configurations and helpers

// Pipeline configuration object
class PipelineConfig {
    String pythonVersion = "3.10"
    String dockerRegistry = "docker.io"
    String dockerRepository = "voice-assistant"
    List<String> supportedBranches = ["main", "master", "develop"]
    Map<String, String> environments = [
        "development": "dev",
        "staging": "staging",
        "production": "prod"
    ]
    
    // Test configuration
    Map<String, String> testDirs = [
        "unit": "tests/unit/",
        "integration": "tests/integration/",
        "e2e": "tests/e2e/",
        "performance": "tests/performance/"
    ]
    
    // Coverage thresholds
    Map<String, Integer> coverageThresholds = [
        "line": 80,
        "branch": 75,
        "function": 80
    ]
}

// Global pipeline configuration
def config = new PipelineConfig()

// ============================================================================
// STAGE RUNNERS
// ============================================================================

/**
 * Run linting checks on the codebase
 */
def runLinting() {
    stage('Linting') {
        try {
            sh '''
                . ./venv/bin/activate
                
                echo "Running Pylint..."
                pylint src/voice_assistant --fail-under=7.0 --exit-zero || true
                
                echo "Running Black formatting check..."
                black --check src/ tests/ || true
                
                echo "Running Flake8..."
                flake8 src/ tests/ --max-line-length=100 --exit-zero || true
                
                echo "Running MyPy type checking..."
                mypy src/voice_assistant --ignore-missing-imports --exit-zero || true
            '''
        } catch (Exception e) {
            echo "Linting stage failed: ${e.message}"
            // Continue pipeline on linting failure
        }
    }
}

/**
 * Run unit tests with coverage reporting
 */
def runUnitTests() {
    stage('Unit Tests') {
        try {
            sh '''
                . ./venv/bin/activate
                pytest tests/unit/ -v \\
                    --cov=src/voice_assistant \\
                    --cov-report=xml \\
                    --cov-report=html \\
                    --cov-report=term \\
                    --junitxml=test-results.xml
            '''
            
            // Publish test results
            junit 'test-results.xml'
            
            // Publish HTML coverage report
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Unit Test Coverage'
            ])
            
            return true
        } catch (Exception e) {
            echo "Unit tests failed: ${e.message}"
            return false
        }
    }
}

/**
 * Run integration tests
 */
def runIntegrationTests() {
    stage('Integration Tests') {
        try {
            sh '''
                . ./venv/bin/activate
                pytest tests/integration/ -v \\
                    --tb=short \\
                    --junitxml=integration-results.xml
            '''
            
            junit 'integration-results.xml'
            return true
        } catch (Exception e) {
            echo "Integration tests failed: ${e.message}"
            return false
        }
    }
}

/**
 * Run E2E tests
 */
def runE2ETests() {
    stage('E2E Tests') {
        try {
            sh '''
                . ./venv/bin/activate
                pytest tests/e2e/ -v \\
                    --tb=short \\
                    --junitxml=e2e-results.xml
            '''
            
            junit 'e2e-results.xml'
            return true
        } catch (Exception e) {
            echo "E2E tests failed: ${e.message}"
            return false
        }
    }
}

/**
 * Run security scanning
 */
def runSecurityScans() {
    stage('Security Scanning') {
        try {
            parallel(
                'Bandit': {
                    sh '''
                        . ./venv/bin/activate
                        echo "Running Bandit security scan..."
                        bandit -r src/voice_assistant -f json -o bandit-report.json || true
                    '''
                },
                'Safety': {
                    sh '''
                        . ./venv/bin/activate
                        echo "Checking for known vulnerabilities..."
                        safety check --json || true
                    '''
                },
                'Pip-Audit': {
                    sh '''
                        . ./venv/bin/activate
                        echo "Auditing Python dependencies..."
                        pip-audit --desc || true
                    '''
                }
            )
            
            // Archive security reports
            archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
            return true
        } catch (Exception e) {
            echo "Security scanning failed: ${e.message}"
            return false
        }
    }
}

/**
 * Run performance tests
 */
def runPerformanceTests() {
    stage('Performance Tests') {
        try {
            sh '''
                . ./venv/bin/activate
                pytest tests/performance/ -v \\
                    --tb=short \\
                    --junitxml=performance-results.xml
            '''
            
            junit 'performance-results.xml'
            return true
        } catch (Exception e) {
            echo "Performance tests failed: ${e.message}"
            return false
        }
    }
}

/**
 * Build Docker image
 */
def buildDockerImage(String tag = "latest") {
    stage('Build Docker Image') {
        try {
            sh '''
                docker build \\
                    -f docker/Dockerfile \\
                    -t ${DOCKER_REPOSITORY}:${tag} \\
                    -t ${DOCKER_REPOSITORY}:latest \\
                    .
            '''
            return true
        } catch (Exception e) {
            echo "Docker build failed: ${e.message}"
            return false
        }
    }
}

/**
 * Push Docker image to registry
 */
def pushDockerImage(String registry = "", String repository = "") {
    stage('Push Docker Image') {
        try {
            registry = registry ?: config.dockerRegistry
            repository = repository ?: config.dockerRepository
            
            sh '''
                echo "Logging into Docker registry..."
                echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin ${registry}
                
                echo "Pushing Docker image..."
                docker push ${registry}/${repository}:latest
                docker push ${registry}/${repository}:${BUILD_NUMBER}
            '''
            return true
        } catch (Exception e) {
            echo "Docker push failed: ${e.message}"
            return false
        }
    }
}

/**
 * Run linting checks in parallel
 */
def runParallelLinting() {
    parallel(
        'Pylint': {
            sh '''
                . ./venv/bin/activate
                pylint src/voice_assistant --fail-under=7.0 --exit-zero || true
            '''
        },
        'Black': {
            sh '''
                . ./venv/bin/activate
                black --check src/ tests/ || true
            '''
        },
        'Flake8': {
            sh '''
                . ./venv/bin/activate
                flake8 src/ tests/ --max-line-length=100 --exit-zero || true
            '''
        },
        'MyPy': {
            sh '''
                . ./venv/bin/activate
                mypy src/voice_assistant --ignore-missing-imports --exit-zero || true
            '''
        }
    )
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Setup Python virtual environment
 */
def setupPythonEnvironment() {
    sh '''
        echo "Setting up Python environment..."
        python --version
        python -m venv venv
        . ./venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements/base.txt
        pip install -r requirements/dev.txt
        pip install -r requirements/test.txt
    '''
}

/**
 * Notify build status
 */
def notifyBuildStatus(String status) {
    def colorCode = status == 'SUCCESS' ? 'good' : 'danger'
    def message = """
    Build ${status}
    Job: ${env.JOB_NAME}
    Build Number: ${env.BUILD_NUMBER}
    Build URL: ${env.BUILD_URL}
    Branch: ${env.GIT_BRANCH}
    Commit: ${env.GIT_COMMIT}
    """
    
    // Slack notification (if configured)
    if (env.SLACK_WEBHOOK_URL) {
        slackSend(
            color: colorCode,
            message: message,
            webhookUrl: env.SLACK_WEBHOOK_URL
        )
    }
    
    // Email notification
    emailext(
        subject: "Build ${status}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: message,
        to: '${DEFAULT_RECIPIENTS}',
        recipientProviders: [developers(), requestor()]
    )
}

/**
 * Check if branch is supported
 */
def isSupportedBranch() {
    def branch = env.GIT_BRANCH.replaceAll('origin/', '')
    return branch in config.supportedBranches
}

/**
 * Check if current build is on main branch
 */
def isMainBranch() {
    def branch = env.GIT_BRANCH.replaceAll('origin/', '')
    return branch == 'main' || branch == 'master'
}

/**
 * Get environment from build parameter
 */
def getEnvironment() {
    return params.ENVIRONMENT ?: 'development'
}

/**
 * Archive test reports
 */
def archiveTestReports() {
    archiveArtifacts artifacts: '*-results.xml', allowEmptyArchive: true
    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
}

// ============================================================================
// EXPORTS
// ============================================================================

return [
    config: config,
    runLinting: this.&runLinting,
    runUnitTests: this.&runUnitTests,
    runIntegrationTests: this.&runIntegrationTests,
    runE2ETests: this.&runE2ETests,
    runSecurityScans: this.&runSecurityScans,
    runPerformanceTests: this.&runPerformanceTests,
    buildDockerImage: this.&buildDockerImage,
    pushDockerImage: this.&pushDockerImage,
    runParallelLinting: this.&runParallelLinting,
    setupPythonEnvironment: this.&setupPythonEnvironment,
    notifyBuildStatus: this.&notifyBuildStatus,
    isSupportedBranch: this.&isSupportedBranch,
    isMainBranch: this.&isMainBranch,
    getEnvironment: this.&getEnvironment,
    archiveTestReports: this.&archiveTestReports
]
