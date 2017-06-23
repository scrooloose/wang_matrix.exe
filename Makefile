install:
	bundle install
	$(MAKE) -C py install

test:
	bundle exec rake spec
	$(MAKE) -C py test
