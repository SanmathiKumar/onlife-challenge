# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'

VAGRANTFILE_API_VERSION = '2'.freeze
PLAYBOOK = 'infrastructure/ansible/playbook-development.yml'.freeze

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define 'development' do |development|
    development.vm.provider :docker do |docker|
      docker.image = 'dockette/vagrant:debian-12'
      docker.has_ssh = true
      docker.pull = true
    end

    development.vm.hostname = 'coding-exercise-vagrant'

    development.vm.provision :ansible do |ansible|
      ansible.playbook = PLAYBOOK
      ansible.compatibility_mode = '2.0'
      ansible.extra_vars = {
        ansible_python_interpreter: '/usr/bin/python3'
      }
    end
  end
end
