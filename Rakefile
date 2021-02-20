require 'rspec/core/rake_task'

namespace :py do
  load "./py/Rakefile"
end

namespace :rb do
  desc "Install Ruby dependencies"
  task :install do
    require 'rubygems'
    require 'bundler/setup'
  end

  RSpec::Core::RakeTask.new(:test)
  task :test => :install
end

desc "Install all dependencies"
task :install => ["rb:install", "py:install"]

desc "Run all tests"
task :test => ["rb:test", "py:test"]

task :default => :test
