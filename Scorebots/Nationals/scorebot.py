
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
Task('Finals','IPTABLES enabled', 5, '[ "$(grep blacklist /etc/modprobe.d/ip_tables.conf)" ]'),
Task('Finals','ettercap removed', 3, '[ ! "$(dpkg --list | grep ettercap)" ]'),
Task('Finals','NX Bit set',1, '[ "$(dmesg | grep NX | grep active)" ]'),
Task('Finals','Bad banner removed', 52 '[ ! "$(grep "HACKED" /etc/motd)" ]'),
Task('Finals','Login.defs login timeout', 2, '[ "$(grep LOGIN_TIMEOUT /etc/login.defs | grep 90)" ]'),
Task('Finals','Login.defs login retries corrected ', 2, '[ ! "$(grep 555 /etc/login.defs)" ]'),
Task('Finals','System uses better ptrace options', 1, '[ "$(grep 0 /proc/sys/kernel/yama/ptrace_scope)" ]'),
Task('Finals','Microarchitectural data sampling enabled to prevent certain issues on certain CPUs', 1, '[ "$(grep mds /etc/default/grub)" ]'),
Task('Finals','iTLB pages forced to be under 4K', 1, '[ "$(grep nx_huge_pages /etc/default/grub)" ]'),
Task('Finals','VSFTPD password in bash history', 2, '[ "$()" ]'),
Task('Finals','Bad shadow hashing algorithm????', 2, '[ "$()" ]'),
Task('Finals','4.5 Million GB zip bomb', 3, '[ "$(grep homeworkFolder.zip /home/cyber/Desktop)" ]')
Task('Finals','BASHRC sudo lockout script', 3, '[ ! "$(grep su /home/cyber/.bashrc)" ]'),
Task('Finals','Samba used old executable version', 2, '[ "$()" ]'),
Task('Finals','Protected Hardlinks', 1, '[ "$(grep 1 /etc/sysctl.d/protect-links.conf)" ]'),
Task('Finals','Immutable Desktop fixed', 5, '[ ! "$(lsattr /home/cyber/Desktop | grep "-e-")" ]')
Task('Finals','train touch script removed', 2, '[ ! "$(ls -al /usr/bin | grep touch | grep 26568)" ]')
#~~~Backdoors~~~#
Task('Finals','FTP 2.3.4 updated)', 5, '[ ! "$(vsftpd -v | grep 2.3.4)" ]'),
Task('Finals','SystemD Sysutils malicious systemd service file fixed', 2, '[ ! "$(ls -l /etc/systemd/system | grep sysutils)" ]'),
Task('Finals','POTT APT backdoor', 2, '[ ! "$(grep "ncat" /etc/apt/apt.conf.d/42backdoor)" ]'),
Task('Finals','Crontab constant reboot script removed', 5, '[ ! "$(grep reboot /var/spool/cron/crontabs/root)" ]')

#~~~Scenario~~~#


#UBUNTU 1
#~~~Forensics~~~#
#~~~Vulnerabilities~~~#
#apt-mark hold 4.15.0-45-generic

Task('Finals','Unneeded ports closed', 5, '[ "$()" ]'),
Task('Finals','Bad umask for BASHRC fixed', 5, '[ "$(grep umask ~/.bashrc | grep 022)" ]'),
Task('Finals','pam permit.so fixed in common-auth', 5, '[ "$(grep requisite /etc/pam.d/common-auth | grep deny)" ]'),
Task('Finals','Hidden root user removed', 5, '[ "$(grep "0\:0" /etc/passwd -c | grep 1)" ]'),
Task('Finals','SUID bit removed on nano', 5, '[ ! "$(stat -c "\%a" /bin/nano | grep 4777)" ]'),
Task('Finals','SUID bit removed on vim', 5, '[ ! "$(stat -c "\%a" /usr/bin/vim.tiny | grep 4777)" ]'),
Task('Finals','Samba script file removed', 5, '[ ! "$(ls -al /home/Public | grep sh)" ]'),
Task('Finals','Samba updated', 5, '[ ! "$(samba -V | grep 4.1.17)" ]'),
Task('Finals','SMB1 disabled', 5, '[ ! "$(grep NT1 /etc/samba/smb.conf)" ]'),
Task('Finals','Bad samba share removed', 5, '[ ! "$(grep Public2 /etc/samba/smb.conf)" ]').
Task('Finals','Samba anonymous accounts disabled', 5, '[ ! "$(grep "map to guest" /etc/samba/smb.conf)" ]'
Task('Finals','Unauthorized samba user removed', 5, '[ ! "$(pdbedit -L | grep simba)" ]'),
Task('Finals','APT Downloads from main server', 5, '[ ! "$(grep unix-solution /etc/apt/sources.list)" ]'),
Task('Finals','System checks for updates', 5, '[ "$(grep "Update-Package-Lists" /etc/apt/apt.conf.d/10periodic| grep 1)" ]'),
Task('Finals','Bad admin removed', 5, '[ ! "$(grep "adm" /etc/group | grep "nadine")" ]'),
Task('Finals','PAM enforces security for passwords', 5, '[ "$(grep "ucredit=‐1 lcredit=‐1 dcredit=‐1 ocredit=‐1" /etc/pam.d/common‐password)" ]'),
Task('Finals','Insecure password fixed', 5, '[ ! "$(grep MeZUTA /etc/shadow)" ]'),
Task('Finals','UFW enabled', 5, '[ "$(ufw status | grep enable)" ]'),
Task('Finals','System stops forkbombs', 5, '[ ! "$(grep "nproc" /etc/security/limits.conf | grep "\#")" ]'),
Task('Finals','SYSCTL IPV4 TIME-WAIT ASSASINATION ENABLED', 5, '[ "$(grep net.ipv4.tcp_rfc1337 /etc/sysctl.conf | grep 1)" ]'),
Task('Finals','SYSCTL TCP Syn Cookies enabled', 5, '[ "$(grep net.ipv4.tcp_syncookie /etc/sysctl.conf | grep 1)" ]'),
Task('Finals','Removed user tac', 5, '[ ! "$(grep tac /etc/passwd)" ]')
Task('Finals','fcrackzip removed', 5, '[ ! "$(dpkg --list | grep fcrackzip)"]'),
#~~~#Webserver~~~#

Task('Finals','Apache2 Sensitive information hidden', 3, ' [ "$(grep ServerSignature /etc/apache2/apache2.conf)" ]'),
Task('Finals','Apache2 mod security WAF installed', 3, ' [ "$(dpkg-query -l libapache2-modsecurity2)" ]'),
#updated
Task('Finals','Apache2 port set', 3, ' [ "$(grep 443 /etc/apache2/ports.conf)" ]'), 
Task('Finals','Apache2 headers tls', 3, ' [ "$(apache2ctl -t -D DUMP_MODULES | grep header)" ]'),
Task('Finals','Apache2 server token info set', 3, ' [ "$(grep ServerTokens /etc/apache2/apache2.conf)" ]'),
Task('Finals','Apache2 follow symlinks', 4,'[ "$(grep AllowOverride /etc/apache2/sites-enabled/000-default.conf | grep Indexes)" ] '),
Task('Finals','Apache2 permissions set', 3, ' ! [ "$(stat -c "%a %n" /etc/apache2/apache2.conf | grep 777)" ]'),
Task('Finals','Apache2 CGI disabled', 3, '! [ "$(apache2ctl -t -D DUMP_MODULES | grep cgi)" ]'), 


Task('Finals','PHP basic information hidden', 2,'[ "$(grep expose_php /etc/mysql/mysql.conf.d/mysqld.cnf | grep -i off)" ]'), 
Task('Finals','PHP dangerous functions are blocked', 2,'[ "$(grep popen /etc/php/7.0/cli/php.ini)" ]'), 
Task('Finals','PHP remote code execution blocked', 2,'[ "$(grep fopen /etc/php/7.0/cli/php.ini | grep -i off)" ]'),
Task('Finals','PHP file uploads enabled', 2,'[ "$(grep file_uploads /etc/php/7.0/cli/php.ini | grep -i on)" ]'),
Task('Finals','PHP dangerously large file upload size fixed', 4,' ! [ "$(grep upload_max_filesize /etc/php/7.0/cli/php.ini | grep -i Gb)" ]'),
Task('Finals','PHP max execution time reduced', 3,' ! [ "$(grep max_execution /etc/php/7.0/cli/php.ini | grep 5000)" ]'),
Task('Finals','PHP Open Base Dir set', 3,' ! [ "$(grep open_basedir /etc/php/7.0/cli/php.ini | grep \';\')" ]'),
#~~~Backdoors~~~#
#!!!# Task('Finals','Anacron job removed', 5, '[ ! "$(grep netcat /etc/cron.d/anacron)" ]'),
Task('Finals','Ubuntu 16.04 Kernel Root Exploit Files removed', 5, '[ ! "$(ls -al /usr/lib | grep 39772)" ]'),
Task('Finals','Kernel Updated', 5, '[ ! "$(uname -a | grep  4.4.0-21-generic)" ]'),
#rootkit hides itself, can't score#Task('Finals','Bad kernel module removed for diamorphine',5, '[ !"$(grep "diamorphine" /proc/modules)" ]')
Task('Finals','POTT Driver backdoor', 5, '[ ! "$(grep "RSHELL" /etc/udev/rules.d/71-vbox-kernel-drivers.rules)" ]'),
Task('Finals','Apache2 mod_backdoor removed', 5, '[ ! "$(apache2ctl -t -D DUMP_MODULES | grep backdoor)" ]'),
#~~~Scenario~~~#

#UBUNTU2
#~~~Forensics~~~#
#~~~Vulnerabilities~~~#
Task('Finals','Among us popup removed', 5, '[ "$()" ]'),
Task('Finals','Firefox blocks popups', 5, '[ "$()" ]'),
Task('Finals','User games cannot be logged into', 5, '[ ! "$(grep games /etc/passwd | grep bash)" ]'),
Task('Finals','empire removed', 5, '[ ! "$(dpkg --list | grep empire)" ]'),
Task('Finals','Syslog should not be writeable by non root users', 5, '[ "$()" ]'),
Task('Finals','Prohibited MP3 files removed', 5, '[ "$()" ]'),
Task('Finals','Martian packets locked', 5, '[ "$(grep net.ipv4.conf.all.log_martians /etc/sysctl.conf | grep 1)" ]'),
Task('Finals','login.defs Max password age set', 5, '[ "$()" ]'),
Task('Finals','Hidden sudoers file removed', 5, '[ "$()" ]'),
Task('Finals','Correct permissions on /etc/passwd set', 5, '[ "$()" ]'),
Task('Finals','/etc/host malicious domain direction fixed', 5, '[ "$()" ]'),
Task('Finals','Sysctl execshield set', 5, '[ "$(grep kernel.exec-shield /etc/sysctl.conf)" ]'),
Task('Finals','protect links', 5, '[ "$(grep 1 /proc/sys/fs/protected_symlinks)" ]'),
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
#Task('Finals','Keylogger Removed', 5, '[ "$()" ]'),
Task('Finals','LD PRELOAD Rootkit removed', 5, '[ ! "$(grep ls /lib | grep libc-vdso.so.6)" ]'),
Task('Finals','UFW backdoored', 5, '[ "$()" ]'),
Task('Finals','POTT BASHRC fake sudo', 5, '[ "$()" ]'),
Task('Finals','POTT SSH backdoored', 5, '[ "$()" ]'),
Task('Finals','Python script that changes passwords removed', 5, '[ "$()" ]')
#~~~Scenario~~~#


