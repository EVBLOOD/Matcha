require 'sinatra'
require 'omniauth'
require 'omniauth-github'

set :bind, '0.0.0.0'

use Rack::Session::Cookie, secret: ENV['SESSION_SECRET']

use OmniAuth::Builder do
  provider :github, ENV['GITHUB_CLIENT_ID'], ENV['GITHUB_CLIENT_SECRET']
end

get '/auth/github/callback' do
  auth = request.env['omniauth.auth']
  email = auth.info.email
  
  redirect "http://back:8080/login/callback?email=#{email}&external=true"
end