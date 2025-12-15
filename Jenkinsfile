pipeline {
    agent any
    
    environment {
        // Python虚拟环境路径
        VENV_DIR = "${WORKSPACE}/venv"
        // Python可执行文件路径（根据Jenkins服务器的Python位置调整）
        PYTHON_CMD = "python3"  // Linux/Mac使用python3，Windows使用python
    }
    
    stages {
        stage('环境检查') {
            steps {
                echo '🔍 检查Python环境...'
                script {
                    if (isUnix()) {
                        sh '''
                            ${PYTHON_CMD} --version
                            ${PYTHON_CMD} -m pip --version
                        '''
                    } else {
                        bat '''
                            python --version
                            python -m pip --version
                        '''
                    }
                }
            }
        }
        
        stage('创建虚拟环境') {
            steps {
                echo '🔧 创建Python虚拟环境...'
                script {
                    if (isUnix()) {
                        sh '''
                            # 删除旧的虚拟环境（如果存在）
                            rm -rf ${VENV_DIR}
                            
                            # 创建新的虚拟环境
                            ${PYTHON_CMD} -m venv ${VENV_DIR}
                            
                            # 激活虚拟环境并升级pip
                            . ${VENV_DIR}/bin/activate
                            pip install --upgrade pip
                        '''
                    } else {
                        bat '''
                            REM 删除旧的虚拟环境（如果存在）
                            if exist venv rmdir /s /q venv
                            
                            REM 创建新的虚拟环境
                            python -m venv venv
                            
                            REM 激活虚拟环境并升级pip
                            call venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                        '''
                    }
                }
            }
        }
        
        stage('安装依赖') {
            steps {
                echo '📦 安装项目依赖...'
                script {
                    if (isUnix()) {
                        sh '''
                            # 激活虚拟环境
                            . ${VENV_DIR}/bin/activate
                            
                            # 安装依赖
                            pip install -r requirements.txt
                            
                            # 显示已安装的包
                            pip list
                        '''
                    } else {
                        bat '''
                            REM 激活虚拟环境
                            call venv\\Scripts\\activate.bat
                            
                            REM 安装依赖
                            pip install -r requirements.txt
                            
                            REM 显示已安装的包
                            pip list
                        '''
                    }
                }
            }
        }
        
        stage('环境配置检查') {
            steps {
                echo '✅ 检查配置文件...'
                script {
                    // 检查关键配置文件是否存在
                    def configFiles = [
                        'config/config.yaml',
                        'grpc_client/explorer_client.py',
                        'grpc_client/generated/explorer/v1/demo_pb2.py',
                        'grpc_client/generated/explorer/v1/demo_pb2_grpc.py'
                    ]
                    
                    configFiles.each { file ->
                        if (fileExists(file)) {
                            echo "✓ ${file} 存在"
                        } else {
                            error "✗ ${file} 不存在，请检查代码库"
                        }
                    }
                }
            }
        }
        
        stage('运行测试') {
            steps {
                echo '🧪 运行自动化测试...'
                script {
                    if (isUnix()) {
                        sh '''
                            # 激活虚拟环境
                            . ${VENV_DIR}/bin/activate
                            
                            # 运行pytest测试
                            pytest tests/ \
                                --html=reports/test_report.html \
                                --self-contained-html \
                                -v \
                                --tb=short \
                                --maxfail=5
                        '''
                    } else {
                        bat '''
                            REM 激活虚拟环境
                            call venv\\Scripts\\activate.bat
                            
                            REM 运行pytest测试
                            pytest tests/ ^
                                --html=reports/test_report.html ^
                                --self-contained-html ^
                                -v ^
                                --tb=short ^
                                --maxfail=5
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo '📊 收集测试报告...'
            // 发布HTML测试报告
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'test_report.html',
                reportName: '自动化测试报告',
                reportTitles: 'gRPC-Web接口测试报告'
            ])
            
            // 清理虚拟环境（可选，如果空间有限）
            // cleanWs()
        }
        
        success {
            echo '✅ 测试执行成功！'
        }
        
        failure {
            echo '❌ 测试执行失败，请查看日志'
        }
    }
}

