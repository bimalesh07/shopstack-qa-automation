pipeline {
    agent any
    
    // 🎛️ Jenkins UI dropdown and inputs configuration
    parameters {
        // 1. Main dropdown for test suites
        choice(
            name: 'TEST_TYPE', 
            choices: ['ALL', 'API', 'DATABASE', 'UI', 'SINGLE_FILE'], 
            description: 'Kya chalana hai? Pura suite, koi ek folder, ya koi single file?'
        )
        // 2. String input field used only when SINGLE_FILE is selected above
        string(
            name: 'SPECIFIC_FILE', 
            defaultValue: '', 
            description: 'Agar upar SINGLE_FILE chuna hai, toh yahan file ka number/naam daalo (e.g., 001, 002, product)'
        )
    }

    // 🔑 Safely importing hidden credentials from Jenkins UI into environment variables
    environment {
        PYTHONIOENCODING     = 'utf-8'
        SECRET_LOCAL_DB_PASS = credentials('SHOPSTACK_DB_PASS_SECRET')
        SECRET_NEON_DB_PASS  = credentials('NEON_DB_PASS_SECRET')
        SECRET_CUST_PASS      = credentials('CUSTOMER_PASS_SECRET')
        SECRET_VEND_PASS      = credentials('VENDOR_PASS_SECRET')
        SECRET_API_PASS       = credentials('API_TEST_PASS_SECRET')
    }

    stages {
        // ⚙️ STAGE 1: Creating python virtual environment and dynamically injecting the fresh .env file
        stage('1. Environment Setup & Recreate .env') {
            steps {
                echo '⚙️ Creating virtual environment and dynamic .env from Jenkins Secrets...'
                bat '''
                    if not exist .venv (
                        python -m venv .venv
                    )
                    call .venv\\Scripts\\activate
                    pip install -r requirements.txt
                    
                    :: Recreating the exact .env file with Windows Batch safety quotes
                    echo SHOPSTACK_BASE_URL=https://shop-stack-ecommerce.vercel.app/ > .env
                    echo SHOPSTACK_DB_HOST=localhost >> .env
                    echo SHOPSTACK_DB_USER=root >> .env
                    echo SHOPSTACK_DB_PASS="%SECRET_LOCAL_DB_PASS%" >> .env
                    echo CUSTOMER_NAME="Bimalesh Kumar" >> .env
                    echo CUSTOMER_EMAIL=bimaleshy49@gmail.com >> .env
                    echo CUSTOMER_PASSWORD="%SECRET_CUST_PASS%" >> .env
                    echo VENDOR_PASSWORD="%SECRET_VEND_PASS%" >> .env
                    echo API_BASE_URL="https://shopstack-ecommerce-1.onrender.com/api" >> .env
                    echo API_TEST_PASSWORD="%SECRET_API_PASS%" >> .env
                    echo DB_HOST=ep-snowy-sea-ap0xzxvv-pooler.c-7.us-east-1.aws.neon.tech >> .env
                    echo DB_PASSWORD="%SECRET_NEON_DB_PASS%" >> .env
                    echo DB_NAME=neondb >> .env
                    echo DB_PORT=5432 >> .env
                '''
            }
        }

        // 🚀 STAGE 2: Smart Execution based on the Dropdown Parameter selected by user
        stage('2. Smart Execution Stage') {
            steps {
                script {
                    def activateVenv = "call .venv\\Scripts\\activate && "
                    
                    // Condition 1: Pura suite ek-ek karke line se chalega
                    if (params.TEST_TYPE == 'ALL') {
                        echo "🚀 Executing ENTIRE Automation Suite one by one..."
                        bat "${activateVenv} pytest --html=target/reports/complete_report.html"
                    } 
                    // Condition 2: Sirf API test folder chalega
                    else if (params.TEST_TYPE == 'API') {
                        echo "🚀 Executing ONLY API Tests..."
                        bat "${activateVenv} pytest test_api/ --html=target/reports/api_report.html"
                    } 
                    // Condition 3: Sirf Database test folder chalega
                    else if (params.TEST_TYPE == 'DATABASE') {
                        echo "🚀 Executing ONLY Database Tests..."
                        bat "${activateVenv} pytest test_database/ --html=target/reports/db_report.html"
                    } 
                    // Condition 4: Sirf UI Web test folder chalega
                    else if (params.TEST_TYPE == 'UI') {
                        echo "🚀 Executing ONLY UI Automation Tests..."
                        bat "${activateVenv} pytest test_ui/ --html=target/reports/ui_report.html"
                    } 
                    // Condition 5: Keyword matching for single file execution (e.g., 001, 002)
                    else if (params.TEST_TYPE == 'SINGLE_FILE') {
                        if (params.SPECIFIC_FILE == '') {
                            error("❌ Error: Bhai, apne SINGLE_FILE chuna par file ka number/naam nahi dala!")
                        } else {
                            echo "🚀 Pytest keyword search matching file for: ${params.SPECIFIC_FILE}"
                            bat "${activateVenv} pytest -k ${params.SPECIFIC_FILE} --html=target/reports/single_file_report.html"
                        }
                    }
                    
                    /* 💡 BADH ME AGAR SMOKE / REGRESSION CHALANA HO TOH KYA KAREN?
                       Jab tum pytest.ini file bana lo, toh upar ke choice parameters mein 'SMOKE' aur 'REGRESSION' add kar dena.
                       Aur unhe chalane ke liye tum bas niche jaisi simple conditions yahan add kar sakte ho:
                       
                       else if (params.TEST_TYPE == 'SMOKE') {
                           bat "${activateVenv} pytest -m smoke --html=target/reports/smoke_report.html"
                       }
                       else if (params.TEST_TYPE == 'REGRESSION') {
                           bat "${activateVenv} pytest -m regression --html=target/reports/regression_report.html"
                       }
                    */
                }
            }
        }
    }

    // 🧹 Post Actions: Security and Test Reporting cleanup
    post {
        always {
            echo '🧹 Security Cleanup: Deleting temporary .env file...'
            bat 'if exist .env del .env'
            
            echo '📊 Archiving Test Reports to Jenkins Dashboard...'
            archiveArtifacts artifacts: 'target/reports/*.html', fingerprint: true, allowEmptyArchive: true
        }
        success {
            echo 'Maza aa gaya bhai! Saare tests PASS ho gaye! 🎉🎉'
        }
        failure {
            echo 'Oops! Kuch tests FAIL ho gaye, please check the console output below. ❌'
        }
    }
}