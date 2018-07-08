from jenkinsapi.jenkins import Jenkins
import sqlite3
conn = sqlite3.connect('C:\sqlite\starseeds.db')
def get_server_instance():
    jenkins_url = 'http://localhost:8080/'
    server = Jenkins(jenkins_url, username = 'jose', password = 'aeiouaeiou')
    return server

"""Get job details of each job that is running on the Jenkins instance and insert them into sql db"""
def get_job_details(server):

    c = conn.cursor()

    c.execute('DELETE FROM jobs')
    
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        print ("*****************")
        print ('Job Name: %s' %(job_instance.name))
        print ('Job Description: %s' %(job_instance.get_description()))
        print ('Is Job running: %s' %(job_instance.is_running()))
        print ('Is Job enabled: %s' %(job_instance.is_enabled()))
        # Insert a row of data

        # job = [( "'"+job_instance.name+"'", "'"+job_instance.get_description()+"'", "'"+job_instance.is_running()+"'", "'"+job_instance.is_enabled()+"'")]
        job = []
        job.append(job_instance.name)
        job.append(job_instance.get_description())
        job.append(job_instance.is_running())
        job.append(job_instance.is_enabled())
        
        c.execute('INSERT INTO jobs VALUES (?, ?, ?, ?)', job)
        # Save (commit) the changes
        conn.commit()
        
    c.execute("SELECT * FROM jobs")
    result = c.fetchall()
    print("SELECT RESULT")
    for job in result:
        print(job)
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


if __name__ == '__main__':
    server = get_server_instance()
    print ("version: ", server.version)
    get_job_details(server)


