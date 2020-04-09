/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
      production: false,
      apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
      auth0: {
          url: 'dev-kaf810lo.auth0.com', // the auth0 domain prefix
          audience: 'coffee', // the audience set for the auth0 app
          clientId: 'G7sE4XDwttOjnNnefC3ATCZ6Isf3Hv71', // the client id generated for the auth0 app
          callbackURL: 'https://localhost:8080/login-results' // the base url of the running ionic application. 
      }
};
