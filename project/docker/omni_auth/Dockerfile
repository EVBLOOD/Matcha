FROM ruby:3.2-slim

RUN apt-get update -y \
    && apt-get install -y build-essential


COPY srcs/omni_auth/Gemfile .

RUN bundle install

WORKDIR /var/www/html


CMD ["ruby", "auth_service.rb"]