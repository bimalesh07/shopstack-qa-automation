"""pipeline {
    agent any 

    environment {
        // 🔥 Tumhaara absolute project directory path
        PROJECT_DIR = 'E:\\ShopStack_Automation_Framework'
        REPORT_TITLE = 'ShopStack Master Automation Test Suite'
    }

    stages {
        // 🟩 STAGE 1: ENVIRONMENT SETUP
        stage('Initialize & Clean Environment') {
            steps {
                echo '⚙️ Spinning up Virtual Env...'
                bat """
                    cd /d "${PROJECT_DIR}"
                    if not exist .venv ( python -m venv .venv )
                """
            }
        }

        // 🟩 STAGE 2: INSTALL DEPENDENCIES
        stage('Install Framework Dependencies') {
            steps {
                echo '📦 Installing required packages...'
                bat """
                    cd /d "${PROJECT_DIR}"
                    call .venv\\Scripts\\activate
                    pip install -r requirements.txt --quiet
                """
            }
        }

        // 🟩 STAGE 3: API TEST EXECUTION
        stage('Execute API Tests') {
            steps {
                echo '🚀 Running Back-End API Tests...'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat """
                        cd /d "${PROJECT_DIR}"
                        call .venv\\Scripts\\activate
                        pytest -v -s Test_Case/test_api/test_003_product_catalog_api.py --html=Reports/api_jenkins_report.html --self-contained-html
                    """
                }
            }
        }

        // 🟩 STAGE 4: PUBLISH REPORT
        stage('Publish Test Reports') {
            steps {
                echo '📊 Deploying HTML graphics to Jenkins...'
                publishHTML([
                    allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true,
                    reportDir: 'Reports', reportFiles: 'api_jenkins_report.html',
                    reportName: 'Pytest API Report', reportTitles: "${REPORT_TITLE}"
                ])
            }
        }
    }
}"""




