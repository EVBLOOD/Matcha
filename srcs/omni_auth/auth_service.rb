require 'sinatra'
require 'omniauth'
require 'omniauth-github'
require 'json'

class AuthApp < Sinatra::Base
    configure do
        set :bind, '0.0.0.0'
        
        set :sessions, true

        use Rack::Session::Cookie, 
            key: 'my_app_session',
            secret: ENV['SESSION_SECRET'],
            httponly: true,
            secure: false,
            domain: ENV['PUBLIC_HOST']

        set :host_authorization, { 
            permitted_hosts: [
              ENV['PUBLIC_HOST'],
              'localhost',
              '127.0.0.1'
            ] 
          }
        OmniAuth.config.full_host = ENV['PUBLIC_BASE_URL']
    end

    OmniAuth.config.request_validation_phase = nil
    use OmniAuth::Builder do
      provider :github, 
        ENV['GITHUB_ID'], 
        ENV['GITHUB_SECRET'],
        
        {
          authorize_params: {
            redirect_uri: ENV['PUBLIC_HOST_redirect'],
            callback_path: '/api/auth/oauth/callback'
          },
            scope: "user:email", 
            callback_path: '/api/auth/oauth/callback',
            provider_ignores_state: true
        }
    end

  get '/api/auth/oauth/callback' do
    puts request.env['omniauth']
    auth = request.env['omniauth.auth']
    puts auth

    halt 400, { error: "Authentication failed" }.to_json unless auth
    infos = auth['info']
    puts infos
    
    content_type :json
    { infos: infos, status: 'authenticated' }.to_json
    end

    get '/auth/failure' do
        "Authentication failed: #{params[:message]}"
    end
end
