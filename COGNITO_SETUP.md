# AWS Cognito Setup Guide

This guide will help you set up AWS Cognito for authentication in the Agentic API application.

## Prerequisites

- An AWS account
- AWS CLI installed and configured (optional, but helpful)
- Basic understanding of AWS services

## Step 1: Create a User Pool

1. Sign in to the AWS Management Console and navigate to the Amazon Cognito service.
2. Click "Create user pool".
3. Choose "Cognito user pool" as the authentication provider.
4. Configure sign-in options:
   - Select "Email" as the primary sign-in option.
   - You can also enable additional options like phone number or username.
5. Configure security requirements:
   - Set password policies according to your security needs.
   - Choose MFA settings (optional but recommended).
   - Configure user account recovery options.
6. Configure sign-up experience:
   - Choose which attributes are required for sign-up.
   - Configure self-service sign-up settings.
   - Set up email or phone verification.
7. Configure message delivery:
   - Choose how verification messages will be sent (via Amazon SES or Cognito's default email service).
8. Integrate your app:
   - Enter a user pool name (e.g., "AgenticAPI-UserPool").
   - Create an app client with a name (e.g., "agentic-api-client").
   - Configure app client settings:
     - Generate a client secret (recommended)
     - Set the callback URL to `http://localhost:8000/auth/callback`
     - Set the sign-out URL to `http://localhost:8000/`
     - Select OAuth 2.0 grant types (Authorization code grant and Refresh token)
     - Select OpenID Connect scopes (email, openid, profile)
9. Review and create the user pool.

## Step 2: Configure the Hosted UI

1. In the AWS Cognito console, select your newly created user pool.
2. Go to the "App integration" tab.
3. Under "App client settings", find your app client.
4. Configure the domain name for the Cognito hosted UI:
   - Choose a domain prefix or use your own domain.
   - For testing, you can use the Cognito domain (e.g., `agentic-api.auth.us-east-1.amazoncognito.com`).
5. Save changes.

## Step 3: Update Environment Variables

Update your `.env` file with the following Cognito-related variables:

```
# AWS Cognito Configuration
AWS_REGION=us-east-1  # Replace with your AWS region
COGNITO_USER_POOL_ID=us-east-1_xxxxxxxx  # Replace with your User Pool ID
COGNITO_APP_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx  # Replace with your App Client ID
COGNITO_DOMAIN=your-domain-prefix.auth.us-east-1.amazoncognito.com  # Replace with your Cognito domain
COGNITO_CALLBACK_URL=http://localhost:8000/auth/callback
COGNITO_LOGOUT_URL=http://localhost:8000/

# JWT Configuration
JWT_SECRET=your_jwt_secret_here  # Generate a secure random string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Step 4: Create Test Users

1. In the AWS Cognito console, select your user pool.
2. Go to the "Users" tab.
3. Click "Create user".
4. Fill in the user details:
   - Username
   - Email address
   - Temporary password or generate one
   - Mark email as verified (for testing purposes)
5. Click "Create user".

## Step 5: Test Authentication

1. Start your application: `python server.py`
2. Open your browser and navigate to `http://localhost:8000/`
3. You should see the login page. Click "Sign in with AWS Cognito".
4. You will be redirected to the Cognito hosted UI.
5. Sign in with the test user credentials.
6. After successful authentication, you will be redirected back to your application.

## Troubleshooting

### Common Issues

1. **Redirect URI Mismatch**: Ensure that the callback URL in your Cognito app client settings exactly matches the one in your application (`http://localhost:8000/auth/callback`).

2. **CORS Issues**: If you encounter CORS errors, make sure your Cognito domain is properly configured and that your application is running on the expected domain/port.

3. **Token Exchange Failures**: Check that your AWS credentials and region are correctly configured in your environment variables.

4. **JWT Verification Errors**: Ensure that your JWT secret is properly set and that the algorithm matches what's specified in your environment variables.

### Debugging Tips

- Enable detailed logging in your application to see the authentication flow.
- Use the AWS Cognito console to monitor user sign-ins and authentication events.
- Check the browser's developer tools for any network or console errors during the authentication process.

## Security Considerations

- In production, always use HTTPS for all URLs.
- Regularly rotate your JWT secret.
- Consider implementing refresh token rotation for enhanced security.
- Set appropriate token expiration times based on your security requirements.
- Implement proper error handling and rate limiting to prevent brute force attacks.

## Additional Resources

- [AWS Cognito Developer Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Documentation](https://jwt.io/introduction/)