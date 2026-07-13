pipeline {
    agent any
    
    parameters {
        choice(
            name: 'TEST_TYPE', 
            choices: ['ALL', 'API', 'DATABASE', 'UI', 'SINGLE_FILE'], 
            description: 'Select the targeted automation execution scope context.'
        )
        string(
            name: 'SPECIFIC_FILE', 
            defaultValue: '', 
            description: 'Specify the test file matching criteria keyword (applicable for SINGLE_FILE only).'
        )
    }
    environment {
        PYTHONIOENCODING     = 'utf-8'
        SECRET_LOCAL_DB_PASS = credentials('SHOPSTACK_DB_PASS_SECRET')
        SECRET_NEON_DB_PASS  = credentials('NEON_DB_PASS_SECRET')
        SECRET_CUST_PASS      = credentials('CUSTOMER_PASS_SECRET')
        SECRET_VEND_PASS      = credentials('VENDOR_PASS_SECRET')
        SECRET_API_PASS       = credentials('API_TEST_PASS_SECRET')
    }
    stages {
        stage('1. Environment Setup & Recreate .env') {
            steps {
                echo 'Initializing virtual environment configuration and runtime properties setup.'
                bat '''
                    if not exist .venv (
                        python -m venv .venv
                    )
                    
                    call .venv\\Scripts\\activate
                    pip install -r requirements.txt
                    
                    echo SHOPSTACK_BASE_URL=https://shop-stack-ecommerce.vercel.app/ > .env
                    echo SHOPSTACK_DB_HOST=localhost >> .env
                    echo SHOPSTACK_DB_PASS="%SECRET_LOCAL_DB_PASS%" >> .env
                    echo DB_HOST=ep-snowy-sea-ap0xzxvv-pooler.c-7.us-east-1.aws.neon.tech >> .env
                    echo DB_USER=neondb_owner >> .env
                    echo DB_NAME=neondb >> .env
                    echo DB_PASSWORD="%SECRET_NEON_DB_PASS%" >> .env
                    echo DB_PORT=5432 >> .env
                    echo CUSTOMER_NAME="Bimalesh Kumar" >> .env
                    echo CUSTOMER_EMAIL=bimaleshy49@gmail.com >> .env
                    echo CUSTOMER_PASSWORD="%SECRET_CUST_PASS%" >> .env
                    echo VENDOR_PASSWORD="%SECRET_VEND_PASS%" >> .env
                    echo API_BASE_URL="https://shopstack-ecommerce-1.onrender.com/api" >> .env
                    echo API_TEST_PASSWORD="%SECRET_API_PASS%" >> .env
                '''
            }
        }

        stage('2. Smart Execution Stage') {
            steps {
                script {
                    def activateVenv = "call .venv\\Scripts\\activate && "
                    
                    if (params.TEST_TYPE == 'ALL') {
                        echo "Triggering global execution for full regression suite repository."
                        bat "${activateVenv} pytest --html=target/reports/complete_report.html"
                    } 
                    else if (params.TEST_TYPE == 'API') {
                        echo "Triggering component execution for backend API integration suites."
                        bat "${activateVenv} pytest Test_Case/test_api/ --html=target/reports/api_report.html"
                    } 
                    else if (params.TEST_TYPE == 'DATABASE') {
                        echo "Triggering component execution for data persistence and validation layers."
                        bat "${activateVenv} pytest Test_Case/test_database/ --html=target/reports/db_report.html"
                    } 
                    else if (params.TEST_TYPE == 'UI') {
                        echo "Triggering component execution for browser user interface tests."
                        bat "${activateVenv} pytest Test_Case/test_ui/ --html=target/reports/ui_report.html"
                    } 
                    else if (params.TEST_TYPE == 'SINGLE_FILE') {
                        if (params.SPECIFIC_FILE == '') {
                            error("Execution aborted: Parameter SPECIFIC_FILE is mandatory when TEST_TYPE is configured to SINGLE_FILE.")
                        } else {
                            echo "Triggering keyword matched filter evaluation profile for: ${params.SPECIFIC_FILE}"
                            bat "${activateVenv} pytest -k ${params.SPECIFIC_FILE} --html=target/reports/single_file_report.html"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleanup Lifecycle: Disposing local environmental file configuration nodes.'
            bat 'if exist .env del .env'
            
            echo 'Reporting Architecture: Archiving targeted compilation artifacts onto dashboard.'
            archiveArtifacts artifacts: 'target/reports/*.html', fingerprint: true, allowEmptyArchive: true
        }
        success {
            echo 'Automation pipeline completed successfully with zero execution regressions.'
        }
        failure {
            echo 'Automation pipeline execution failed. Review the targeted step console logs for failure trace diagnostic matrix.'
        }
    }
}