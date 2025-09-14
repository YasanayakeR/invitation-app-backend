# Backend Deployment Guide

## Prerequisites
- MongoDB Atlas account with cluster set up
- Git repository
- Hosting platform account (Heroku, Railway, Render, or DigitalOcean)

## Step 1: Set Up MongoDB Atlas

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account

2. **Create a Cluster**
   - Choose "Build a Database" 
   - Select "Shared" (free tier)
   - Choose your preferred cloud provider and region
   - Create cluster

3. **Configure Database Access**
   - Go to "Database Access" in left sidebar
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Create username and password
   - Set "Built-in Role" to "Read and write to any database"

4. **Configure Network Access**
   - Go to "Network Access" in left sidebar
   - Click "Add IP Address"
   - Select "Allow Access from Anywhere" (for deployment)
   - Confirm

5. **Get Connection String**
   - Go to "Database" in left sidebar
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password

## Step 2: Environment Variables

Create a `.env` file with your MongoDB Atlas URL:

```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/your_database_name?retryWrites=true&w=majority
DB_NAME=your_database_name
ADMIN_PASSCODE=your_secure_admin_passcode
JWT_SECRET_KEY=your_very_secure_jwt_secret_key_change_this
```

## Step 3: Deployment Options

### Option A: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set MONGO_URI="your_mongodb_atlas_connection_string"
   heroku config:set DB_NAME="your_database_name"
   heroku config:set ADMIN_PASSCODE="your_secure_passcode"
   heroku config:set JWT_SECRET_KEY="your_jwt_secret"
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

### Option B: Deploy to Railway

1. **Go to [Railway](https://railway.app)**
2. **Sign up with GitHub**
3. **Create New Project**
4. **Deploy from GitHub repo**
5. **Add Environment Variables** in Railway dashboard:
   - `MONGO_URI`
   - `DB_NAME`
   - `ADMIN_PASSCODE`
   - `JWT_SECRET_KEY`

### Option C: Deploy to Render

1. **Go to [Render](https://render.com)**
2. **Sign up with GitHub**
3. **Create New Web Service**
4. **Connect GitHub repository**
5. **Configure:**
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
6. **Add Environment Variables**

### Option D: Deploy with Docker

1. **Build Docker Image**
   ```bash
   docker build -t your-app-name .
   ```

2. **Run Locally (Test)**
   ```bash
   docker run -p 8000:8000 \
     -e MONGO_URI="your_connection_string" \
     -e DB_NAME="your_db_name" \
     -e ADMIN_PASSCODE="your_passcode" \
     -e JWT_SECRET_KEY="your_secret" \
     your-app-name
   ```

3. **Deploy to any Docker-compatible platform**

## Step 4: Test Your Deployment

1. **Check Health**
   ```bash
   curl https://your-app-url.com/health
   ```

2. **Test Admin Login**
   ```bash
   curl -X POST https://your-app-url.com/admin/login \
     -H "Content-Type: application/json" \
     -d '{"passcode": "your_passcode"}'
   ```

3. **Test Protected Endpoint**
   ```bash
   curl -X GET https://your-app-url.com/users/ \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Step 5: Production Considerations

1. **Security:**
   - Change default passcode
   - Use strong JWT secret key
   - Enable HTTPS
   - Restrict MongoDB network access to your hosting platform

2. **Monitoring:**
   - Set up application monitoring
   - Configure error logging
   - Monitor database performance

3. **Scaling:**
   - Configure auto-scaling if needed
   - Monitor resource usage
   - Set up backup strategies

## API Endpoints

Once deployed, your API will have these endpoints:

- `POST /admin/login` - Admin authentication
- `POST /users/` - Create user (public)
- `GET /users/` - List users (admin only)
- `GET /docs` - API documentation
- `GET /health` - Health check

## Troubleshooting

**Common Issues:**

1. **MongoDB Connection Error**
   - Check connection string format
   - Verify database user credentials
   - Ensure network access is configured

2. **Environment Variables Not Loading**
   - Verify variable names match exactly
   - Check hosting platform environment variable settings

3. **Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

4. **Port Issues**
   - Hosting platforms assign dynamic ports
   - Use `PORT` environment variable in production
