test:
	bundle exec rake spec
	$(MAKE) -C py test
