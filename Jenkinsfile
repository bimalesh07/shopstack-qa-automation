pipeline {
    // Jenkins ko bol rahe hain ki kisi bhi khali terminal/machine par test chala do
    agent any
    
    // 🎛️ Yeh hissa Jenkins UI par dropdown aur box banata hai
    parameters {
        // 1. Choice parameter se dropdown banta hai
        choice(
            name: 'TEST_TYPE', 
            choices: ['ALL', 'API', 'DATABASE', 'UI', 'SINGLE_FILE'], 
            description: 'Bhai dropdown se chunlo kya chalana hai: Pura suite, koi ek folder, ya single file?'
        )
        // 2. String parameter se text box banta hai (sirf SINGLE_FILE ke liye)
        string(
            name: 'SPECIFIC_FILE', 
            defaultValue: '', 
            description: 'Agar upar SINGLE_FILE chuna hai, toh yahan keyword daalo (jaise: *database*)'
        )
    }

    // 🔑 Jenkins ke dashboard se chhupe huye passwords utha kar yahan variables mein daal rahe hain
    environment {
        PYTHONIOENCODING     = 'utf-8' // Emojis ke crash ko rokne ke liye encoding set ki hai
        SECRET_LOCAL_DB_PASS = credentials('SHOPSTACK_DB_PASS_SECRET')
        SECRET_NEON_DB_PASS  = credentials('NEON_DB_PASS_SECRET')
        SECRET_CUST_PASS      = credentials('CUSTOMER_PASS_SECRET')
        SECRET_VEND_PASS      = credentials('VENDOR_PASS_SECRET')
        SECRET_API_PASS       = credentials('API_TEST_PASS_SECRET')
    }

    stages {
        // ⚙️ STAGE 1: Python ka setup karna aur nayi .env file taiyar karna
        stage('1. Environment Setup & Recreate .env') {
            steps {
                echo '⚙️ Virtual environment ban raha hai aur fresh .env file likhi jaa rahi hai...'
                bat '''
                    :: Agar .venv folder nahi hai, toh naya banao
                    if not exist .venv (
                        python -m venv .venv
                    )
                    
                    :: Virtual environment ko activate karke saare requirements install karo
                    call .venv\\Scripts\\activate
                    pip install -r requirements.txt
                    
                    :: 📑 Yahan se ek ek karke .env file ke andar settings likhi jaa rahi hain
                    :: single '>' ka matlab purani file delete karke nayi shuruat karo
                    echo SHOPSTACK_BASE_URL=https://shop-stack-ecommerce.vercel.app/ > .env
                    
                    :: '>>' ka matlab isi file ke niche lines jodte chale jao
                    :: 🔌 Local & Cloud Database ki settings (Variables perfectly matched)
                    echo SHOPSTACK_DB_HOST=localhost >> .env
                    echo SHOPSTACK_DB_PASS="%SECRET_LOCAL_DB_PASS%" >> .env
                    echo DB_HOST=ep-snowy-sea-ap0xzxvv-pooler.c-7.us-east-1.aws.neon.tech >> .env
                    echo DB_USER=neondb_owner >> .env
                    echo DB_NAME=neondb >> .env
                    echo DB_PASSWORD="%SECRET_NEON_DB_PASS%" >> .env
                    echo DB_PORT=5432 >> .env
                    
                    :: 🔐 UI aur API login ke liye baki bache credentials
                    echo CUSTOMER_NAME="Bimalesh Kumar" >> .env
                    echo CUSTOMER_EMAIL=bimaleshy49@gmail.com >> .env
                    echo CUSTOMER_PASSWORD="%SECRET_CUST_PASS%" >> .env
                    echo VENDOR_PASSWORD="%SECRET_VEND_PASS%" >> .env
                    echo API_BASE_URL="https://shopstack-ecommerce-1.onrender.com/api" >> .env
                    echo API_TEST_PASSWORD="%SECRET_API_PASS%" >> .env
                '''
            }
        }

        // 🚀 STAGE 2: Dropdown mein tumne jo chuna, uske hisab se sahi command chalana
        stage('2. Smart Execution Stage') {
            steps {
                script {
                    // Python virtual environment activate karne ka shortcut variable
                    def activateVenv = "call .venv\\Scripts\\activate && "
                    
                    // Agar dropdown mein 'ALL' chuna hai, toh saare tests chalao
                    if (params.TEST_TYPE == 'ALL') {
                        echo "🚀 Pura ke pura Automation Suite ek sath chal raha hai..."
                        bat "${activateVenv} pytest --html=target/reports/complete_report.html"
                    } 
                    // Agar dropdown mein 'API' chuna hai, toh sirf test_api waala folder chalao
                    else if (params.TEST_TYPE == 'API') {
                        echo "🚀 Sirf API wale tests chal rahe hain..."
                        bat "${activateVenv} pytest Test_Case/test_api/ --html=target/reports/api_report.html"
                    } 
                    // Agar dropdown mein 'DATABASE' chuna hai, toh Test_Case folder ke andar ka database folder chalao
                    else if (params.TEST_TYPE == 'DATABASE') {
                        echo "🚀 Sirf Database wale tests chal rahe hain..."
                        bat "${activateVenv} pytest Test_Case/test_database/ --html=target/reports/db_report.html"
                    } 
                    // Agar dropdown mein 'UI' chuna hai, toh sirf web UI automation chalao
                    else if (params.TEST_TYPE == 'UI') {
                        echo "🚀 Sirf Browser wale UI tests chal rahe hain..."
                        bat "${activateVenv} pytest Test_Case/test_ui/ --html=target/reports/ui_report.html"
                    } 
                    // Agar dropdown mein 'SINGLE_FILE' chuna hai, toh box mein likhe naam (jaise: *database*) se dhundh kar chalao
                    else if (params.TEST_TYPE == 'SINGLE_FILE') {
                        // Agar box khali chhod diya toh error de do
                        if (params.SPECIFIC_FILE == '') {
                            error("❌ Arrey bhai! SINGLE_FILE chuna hai toh niche box mein file ka naam toh daalo!")
                        } else {
                            echo "🚀 Pytest se tumhari chuninda file search karke chala rahe hain: ${params.SPECIFIC_FILE}"
                            bat "${activateVenv} pytest -k ${params.SPECIFIC_FILE} --html=target/reports/single_file_report.html"
                        }
                    }
                }
            }
        }
    }

    // 🧹 Post Actions: Test khatam hone ke baad safai karna aur report bachana
    post {
        always {
            // Security ke liye temporary bani .env file ko delete kar rahe hain taaki password leak na ho
            echo '🧹 Security Safai: Kaam khatam, ab temporary .env file delete kar rahe hain...'
            bat 'if exist .env del .env'
            
            // HTML Report ko Jenkins dashboard par permanent save (archive) kar rahe hain
            echo '📊 HTML Reports ko utha kar Jenkins Dashboard par chipka rahe hain...'
            archiveArtifacts artifacts: 'target/reports/*.html', fingerprint: true, allowEmptyArchive: true
        }
        success {
            echo 'Maza aa gaya bhai! Saare tests ekdum makkhan PASS ho gaye! 🎉🎉'
        }
        failure {
            echo 'Dhat teri ki! Kuch tests FAIL ho gaye, upar console output check karo. ❌'
        }
    }
}