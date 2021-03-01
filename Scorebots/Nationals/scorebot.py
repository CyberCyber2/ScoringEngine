#Task('Finals',' ', 5, '[ "$()" ]')

#DEBIAN
#~~~Forensics~~~#
#~~~Vulnerabilities~~~#
Task('Finals','Removed bad apt-hold setting for iptables', 5, '[ ! "$(apt-mark showhold iptables)" ]'),
Task('Finals','Hidden Sudoers config removed', 5, '[ "$()" ]'),
Task('Finals','VSFTPD uses SSL/TLS', 5, '[ "$()" ]'),
Task('Finals','VSFTPD no longer allows anonymous logins', 5, '[ "$()" ]'),
Task('Finals','VSFTPD blocks unauthorized users', 5, '[ "$()" ]'),
Task('Finals','VSFTPD Bruteforce fixed via IPTABLES rules', 5, '[ "$()" ]'),
Task('Finals','Hidden VSFTPD file removed with passwords', 5, '[ "$()" ]'),
Task('Finals','VSFTPD listening on correct port', 5, '[ "$()" ]')
Task('Finals','IPTABLES enabled', 5, '[ "$()" ]'),
Task('Finals','ettercap removed', 5, '[ ! "$(dpkg --list | grep ettercap)" ]'),
Task('Finals','NX Bit set', 5, '[ "$(dmesg | grep NX | grep active)" ]'),
Task('Finals','Bad banner removed', 5, '[ "$()" ]'),
Task('Finals','Login.defs secure hashing algorithm', 5, '[ "$()" ]'),
Task('Finals','Login.defs logs failed logins', 5, '[ "$()" ]'),
Task('Finals','System uses better ptrace options', 5, '[ "$(grep 0 /proc/sys/kernel/yama/ptrace_scope || grep 0 /etc/sysctl.d/10-ptrace.conf)" ]'),
Task('Finals','Microdata sampling enabled', 5, '[ "$(grep mds=off /etc/default/grub)" ]'),
Task('Finals','iTLB pages forced to be under 4K', 5, '[ "$(grep nx_huge_pages /etc/default/grub)" ]'),
Task('Finals','VSFTPD password in bash history', 5, '[ "$()" ]'),
Task('Finals','Bad shadow hashing algorithm????', 5, '[ "$()" ]'),
Task('Finals','4.5 Million GB zip bomb', 1, '[ "$(grep homeworkFolder.zip /home/cyber/Desktop)" ]')
#~~~Backdoors~~~#
Task('Finals','FTP 2.3.4 updated)', 5, '[ ! "$(vsftpd -v | grep 2.3.4)" ]'),
Task('Finals','SystemD Sysutils malicious systemd service file fixed', 5, '[ ! "$(ls -l /etc/systemd/system | grep sysutils)" ]'),
#~~~Scenario~~~#


#UBUNTU 1
#~~~Forensics~~~#
#~~~Vulnerabilities~~~#
#apt-mark hold 4.15.0-45-generic

Task('Finals','Unneeded ports closed', 5, '[ "$()" ]'),
Task('Finals','Bad uname for BASHRC fixed', 5, '[ "$()" ]'),
Task('Finals','pam permit.so fixed in common-auth', 5, '[ "$()" ]'),
Task('Finals','Hidden root user removed', 5, '[ "$()" ]'),
Task('Finals','SUID bit removed on nano', 5, '[ "$()" ]'),
Task('Finals','SUID bit removed on vim', 5, '[ "$()" ]'),
Task('Finals','Samba password file removed', 5, '[ "$()" ]'),
Task('Finals','Samba updated', 5, '[ "$()" ]'),
Task('Finals','SMB1 disabled', 5, '[ "$()" ]'),
Task('Finals','Bad samba share removed', 5, '[ "$()" ]').
Task('Finals','Samba anonymous accounts disabled', 5, '[ "$()" ]'
Task('Finals','Unauthorized samba user removed', 5, '[ "$()" ]'),
Task('Finals','APT Downloads from main server', 5, '[ "$()" ]'),
Task('Finals','System checks for updates', 5, '[ "$()" ]'),
Task('Finals','Bad admin removed', 5, '[ "$()" ]'),
Task('Finals','PAM enforces security for passwords', 5, '[ "$()" ]'),
Task('Finals','Insecure password fixed', 5, '[ "$()" ]'),
Task('Finals','User games cannot be logged into', 5, '[ "$()" ]'),
Task('Finals','UFW enabled', 5, '[ "$()" ]'),
Task('Finals','System stops forkbombs', 5, '[ "$()" ]'),
Task('Finals','SYSCTL IPV4 TIME-WAIT ASSASINATION ENABLED', 5, '[ "$()" ]'),
Task('Finals','SYSCTL TCP Syn Cookies enabled', 5, '[ "$()" ]'),
Task('Finals','Removed user tac', 5, '[ "$()" ]')
Task('Finals','fcrackzip removed', 5, '[ ! "$(dpkg --list | grep fcrackzip)"]'),
#~~~#Webserver~~~#
Task('Finals','PHP basic information hidden', 2,'[ "$(grep expose_php /etc/mysql/mysql.conf.d/mysqld.cnf | grep -i off)" ]'), 
Task('Finals','PHP dangerous functions are blocked', 2,'[ "$(grep popen /etc/php/7.0/cli/php.ini)" ]'), #There are more things, but too lazy to score 
Task('Finals','PHP remote code execution blocked', 2,'[ "$(grep fopen /etc/php/7.0/cli/php.ini | grep -i off)" ]'),
Task('Finals','PHP file uploads enabled', 2,'[ "$(grep file_uploads /etc/php/7.0/cli/php.ini | grep -i on)" ]'),
Task('Finals','PHP dangerously large file upload size fixed', 4,' ! [ "$(grep upload_max_filesize /etc/php/7.0/cli/php.ini | grep -i Gb)" ]'),
Task('Finals','PHP max execution time reduced', 3,' ! [ "$(grep max_execution /etc/php/7.0/cli/php.ini | grep 5000)" ]'),
Task('Finals','PHP Open Base Dir set', 3,' ! [ "$(grep open_basedir /etc/php/7.0/cli/php.ini | grep \';\')" ]'),

Task('Finals','Apache2 mod_rootme removed', 5, '[ "$()" ]'),
Task('Finals',' ', 5, '[ "$()" ]')
#~~~Backdoors~~~#
Task('Finals','Anacron job removed', 5, '[ ! "$(grep netcat /etc/cron.d/anacron)" ]'),
Task('Finals','Ubuntu 16.04 Kernel Root Exploit Files removed', 5, '[ ! "$(ls -al /usr/lib | grep 39772)" ]'),
Task('Finals','Kernel Updated', 5, '[ ! "$(uname -a | grep  4.4.0-21-generic)" ]'),
Task('Bad kernel module removed for netcat',' ', 5, '[ !"$(grep "pink" /proc/modules)" ]')
#~~~Scenario~~~#

#UBUNTU2
#~~~Forensics~~~#
#~~~Vulnerabilities~~~#
Task('Finals','Among us popup removed', 5, '[ "$()" ]'),
Task('Finals','Firefox blocks popups', 5, '[ "$()" ]'),
Task('Finals','empire removed', 5, '[ ! "$(dpkg --list | grep empire)" ]'),
Task('Finals','Syslog should not be writeable by non root users', 5, '[ "$()" ]'),
Task('Finals','Prohibited MP3 files removed', 5, '[ "$()" ]'),
Task('Finals','Martian packets locked', 5, '[ "$(grep net.ipv4.conf.all.log_martians /etc/sysctl.conf | grep 1)" ]'),
Task('Finals','login.defs Max password age set', 5, '[ "$()" ]'),
Task('Finals','Hidden sudoers file removed', 5, '[ "$()" ]'),
Task('Finals','Correct permissions on /etc/passwd set', 5, '[ "$()" ]'),
Task('Finals','/etc/host malicious domain direction fixed', 5, '[ "$()" ]'),
Task('Finals','Sysctl execshield set', 5, '[ "$(grep kernel.exec-shield /etc/sysctl.conf)" ]'),
Task('Finals','malicious alias removed', 5, '[ "$(grep 1 /proc/sys/fs/protected_symlinks)" ]'),
Task('Finals','Limits.conf coredumps restricted', 5, '[ "$((grep \'hard core\' /etc/security/limits.conf)" ]'),
Task('Finals','TCToUR via symlinks and hardlinks fixed', 5, '[ "$()" ]'),
Task('Finals','SSHD X11 forwarding disabled', 5, '[ "$(grep X11Forwarding /etc/ssh/sshd_config | grep no)" ]'),
Task('Finals','SSHD prevents root login', 5, '[ "$(grep PermitRoot /etc/ssh/sshd_config | grep n)" ]'),
Task('Finals','SSHD correct protocol set', 5, '[ "$(grep Protocol /etc/ssh/sshd_config | grep 2)" ]'),
Task('Finals','Bad permission on SSH keys directory removed', 5, '[ "$()" ]'),
Task('Finals','Bad Crontab removed', 5, '[ "$()" ]'),
Task('Finals','Insecure protocol DECNET blocked to non system accounts', 5, '[ "$(grep net-pf-12 /etc/modprobe.d/blacklist-rare-network.conf | grep off)" ]'),
Task('Finals','APT netcat installation removed', 5, '[ "$()" ]')
#~~~Backdoors~~~#
Task('Finals','Data exfiltration script removed for /etc/passwd', 5, '[ "$()" ]')
Task('Finals','Keylogger Removed', 5, '[ "$()" ]'),
Task('Finals','LD PRELOAD Rootkit removed removed', 5, '[ ! "$(grep ls /lib | grep libc-vdso.so.6)" ]')
#~~~Scenario~~~#
