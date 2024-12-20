# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.boot_timeout = 1000
  config.vm.box_check_update = true
  config.vbguest.auto_update = false if Vagrant.has_plugin?('vagrant-vbguest')

  config.vm.define "master" do |master|
    master.vm.network "forwarded_port", guest: 22, host: 60030, auto_correct: true, id: "ssh"
    master.vm.network "private_network", ip: "192.168.1.10"
	master.vm.hostname = "master"
    master.vm.provider "virtualbox" do |vb|
	  vb.name = "k8s-master"
      vb.memory = 2048
	  vb.cpus = 2
	  vb.gui = true
    end
	
	master.vm.provision "shell", inline: "apt update -y"
	master.vm.provision "shell", inline: "apt install ansible -y"
	
    master.vm.provision "ansible_local" do |ansible|
	  ansible.compatibility_mode = "2.0"  # 호환성 모드 설정
	  ansible.become = true
      ansible.playbook = "playbook.yml"
      ansible.groups = {
        "masters" => ["master"]
      }
    end
	# 디렉토리 권한 수정
	master.vm.provision "shell", inline: <<-SHELL
	  sudo chmod o-w /vagrant
	SHELL
  end

  config.vm.define "worker1" do |worker1|
    worker1.vm.network "forwarded_port", guest: 22, host: 60031, auto_correct: true, id: "ssh"
    worker1.vm.network "private_network", ip: "192.168.1.11"
	worker1.vm.hostname = "worker1"
    worker1.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-worker1"
      vb.memory = 2048
	  vb.cpus = 1
	  vb.gui = true
    end
	
	worker1.vm.provision "shell", inline: "apt update -y"
	worker1.vm.provision "shell", inline: "apt install ansible -y"
	
	
    worker1.vm.provision "ansible_local" do |ansible|
	  ansible.compatibility_mode = "2.0"  # 호환성 모드 설정
	  ansible.become = true
      ansible.playbook = "playbook.yml"
      ansible.groups = {
        "workers" => ["worker1"]
      }
    end
	# 디렉토리 권한 수정
	worker1.vm.provision "shell", inline: <<-SHELL
	  sudo chmod o-w /vagrant
	SHELL
  end


  config.vm.define "worker2" do |worker2|
    worker2.vm.network "forwarded_port", guest: 22, host: 60032, auto_correct: true, id: "ssh"
    worker2.vm.network "private_network", ip: "192.168.1.12"
	worker2.vm.hostname = "worker2"
    worker2.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-worker2"
      vb.memory = 2048
	  vb.cpus = 1
	  vb.gui = true
    end
	
	worker2.vm.provision "shell", inline: "apt update -y"
	worker2.vm.provision "shell", inline: "apt install ansible -y"
	
	
    worker2.vm.provision "ansible_local" do |ansible|
	  ansible.compatibility_mode = "2.0"  # 호환성 모드 설정
	  ansible.become = true
      ansible.playbook = "playbook.yml"
      ansible.groups = {
        "workers" => ["worker2"]
      }
    end
	# 디렉토리 권한 수정
	worker2.vm.provision "shell", inline: <<-SHELL
	  sudo chmod o-w /vagrant
	SHELL
  end
  
  config.vm.define "worker3" do |worker3|
    worker3.vm.network "forwarded_port", guest: 22, host: 60033, auto_correct: true, id: "ssh"
    worker3.vm.network "private_network", ip: "192.168.1.13"
	worker3.vm.hostname = "worker3"
    worker3.vm.provider "virtualbox" do |vb|
	  vb.name = "k8s-worker3"
      vb.memory = 2048
	  vb.cpus = 1
	  vb.gui = true
    end
	
	worker3.vm.provision "shell", inline: "apt update -y"
	worker3.vm.provision "shell", inline: "apt install ansible -y"
	
    worker3.vm.provision "ansible_local" do |ansible|
	  ansible.compatibility_mode = "2.0"  # 호환성 모드 설정
	  ansible.become = true
      ansible.playbook = "playbook.yml"
      ansible.groups = {
        "workers" => ["worker3"]
      }
    end
	# 디렉토리 권한 수정
	worker3.vm.provision "shell", inline: <<-SHELL
	  sudo chmod o-w /vagrant
	SHELL
  end
end
