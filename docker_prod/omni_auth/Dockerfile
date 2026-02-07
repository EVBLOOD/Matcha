FROM ruby:3.2-slim

RUN apt-get update -y \
    && apt-get install -y build-essential


COPY srcs/omni_auth/Gemfile .

RUN bundle install

WORKDIR /var/www/html

ENV RAILS_ENV=development

# CMD ["ruby", "app.rb", "-o", "0.0.0.0"]
CMD ["bundle", "exec", "rerun", "--background", "--", "rackup", "-o", "0.0.0.0", "-p", "4567", "config.ru"]