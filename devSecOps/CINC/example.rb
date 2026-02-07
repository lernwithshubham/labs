control 'web-server-hardening' do
  impact 1.0
  title 'Web Server Security Checks'

  # Check 1: Software Availability
  describe package('nginx') do
    it { should be_installed }
  end

  # Check 2: Critical File Permissions
  describe file('/etc/shadow') do
    it { should exist }
    it { should be_owned_by 'root' }
  end

  # Check 3: Malware Detection
  describe file('/tmp/backdoor.sh') do
    it { should_not exist }
  end
end