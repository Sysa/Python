NodeForCleanup = getProperty('NodeForCleanup') //test-integration
kl_value = getProperty('kl')
ttl_value = getProperty('ttl')
PathForCleanup = getProperty('PathForCleanup') //PathForCleanup //C:/SharedSpace/cleanup_files_check/
venv = getProperty('venv') //C:\\_cron_jobs\\venv_jnk_backup_v2
python_exec_path = getProperty('python_exec_path') //C:\\Users\\khlopov\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe
EmailToReport = getProperty('EmailToReport')
EmailToReport = EmailToReport.replace("\n", ",")

node(NodeForCleanup){
	stage('Checkout script'){
		git changelog: false, credentialsId: 'git_bot', poll: false, url: 'http://localhost:8080/scm/aut/utilities.git'
	}
    stage('Running cleanup command'){
        echo kl_value
		echo "workspace is" + env.WORKSPACE
		pathToScript = env.WORKSPACE + "\\cleanup\\"
		echo pathToScript
        //"C:\Users\khlopov\AppData\Local\Programs\Python\Python37-32\python.exe" -m venv "C:\_cron_jobs\venv_jnk_backup_v2" && "C:\_cron_jobs\venv_jnk_backup_v2\Scripts\python.exe" -m pip install --upgrade pip && "C:\_cron_jobs\venv_jnk_backup_v2\Scripts\pip" install -r "C:\_cron_jobs\requirements.txt" && "C:\_cron_jobs\venv_jnk_backup_v2\Scripts\python.exe" "C:\_cron_jobs\do_cleanup.py" --path "C:/SharedSpace/cleanup_files_check/" --ttl "0" --kl "5"
		//"C:\\Users\\khlopov\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe" -m venv "C:\\_cron_jobs\\venv_jnk_backup_v2" && "C:\\_cron_jobs\\venv_jnk_backup_v2\\Scripts\\python.exe" -m pip install --upgrade pip && "C:\\_cron_jobs\\venv_jnk_backup_v2\\Scripts\\pip" install -r "C:\\_cron_jobs\\requirements.txt" && "C:\\_cron_jobs\\venv_jnk_backup_v2\\Scripts\\python.exe" "C:\\_cron_jobs\\do_cleanup.py" --path "C:/SharedSpace/cleanup_files_check/" --ttl "0" --kl "'''+kl_value+'''"
        sh '''
        echo '''+kl_value+'''
        "'''+python_exec_path+'''" -m venv "'''+venv+'''" && "'''+venv+'''\\Scripts\\python.exe" -m pip install --upgrade pip && "'''+venv+'''\\Scripts\\pip" install -r "'''+pathToScript+'''\\requirements.txt" && "'''+venv+'''\\Scripts\\python.exe" "'''+pathToScript+'''\\do_cleanup.py" --path "'''+PathForCleanup+'''" --ttl "'''+ttl_value+'''" --kl "'''+kl_value+'''" --emails "'''+EmailToReport+'''" --job_url "'''+env.JOB_URL+'''"
        '''
    }
}
