with open("server.log", "w") as file:
  file.write("Nov 12 14:33:01 server sshd[1201]: Failed password for root from 177.233.10.45 port 45821 ssh2\n")
  file.write("Nov 12 14:34:05 server sshd[1202]: Accepted password for user1 from 192.168.0.10 port 52345 ssh2\n")
  file.write("Nov 12 14:35:11 server sshd[1203]: Failed password for admin from 177.233.10.45 port 45822 ssh2\n")
  file.write("Nov 12 14:36:00 server sshd[1204]: Connection closed by 192.168.0.11\n")
  file.write("Nov 12 14:36:50 server sshd[1205]: Failed password for root from 10.0.0.5 port 50231 ssh2\n")


  def ler_logs(caminho):
    with open('caminho', 'r') as file:
      linhas = file.readlines()
      

