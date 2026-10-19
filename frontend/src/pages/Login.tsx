import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading, error: authError } = useAuth();
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Login form state
  const [loginForm, setLoginForm] = useState({
    username: '',
    password: '',
  });

  // Register form state
  const [registerForm, setRegisterForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
  });

  const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginForm({
      ...loginForm,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegisterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRegisterForm({
      ...registerForm,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(loginForm.username, loginForm.password);
      navigate('/dashboard');
    } catch (err) {
      setError(authError || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (registerForm.password !== registerForm.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (registerForm.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/users/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          full_name: registerForm.fullName || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      setSuccess('Registration successful! Logging you in...');
      setTimeout(() => {
        login(registerForm.username, registerForm.password).then(() => {
          navigate('/dashboard');
        });
      }, 1000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center p-4">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-md"
      >
        {/* Logo/Header */}
        <motion.div variants={itemVariants} className="text-center mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400 mb-2">
            DataScientist Arena
          </h1>
          <p className="text-gray-400">AI Reliability Testing Platform</p>
        </motion.div>

        {/* Auth Card */}
        <motion.div
          variants={itemVariants}
          className="bg-gray-800/50 border border-gray-700 rounded-xl p-8 backdrop-blur-sm"
        >
          {/* Tabs */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => {
                setIsLoginMode(true);
                setError(null);
                setSuccess(null);
              }}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
                isLoginMode
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              Login
            </button>
            <button
              onClick={() => {
                setIsLoginMode(false);
                setError(null);
                setSuccess(null);
              }}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
                !isLoginMode
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              Sign Up
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 p-3 bg-red-900/30 border border-red-700/50 rounded-lg text-red-400 text-sm"
            >
              {error}
            </motion.div>
          )}

          {/* Success Message */}
          {success && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 p-3 bg-green-900/30 border border-green-700/50 rounded-lg text-green-400 text-sm"
            >
              {success}
            </motion.div>
          )}

          {/* Login Form */}
          {isLoginMode && (
            <motion.form
              key="login"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              onSubmit={handleLogin}
              className="space-y-4"
            >
              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  value={loginForm.username}
                  onChange={handleLoginChange}
                  placeholder="Enter your username"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  value={loginForm.password}
                  onChange={handleLoginChange}
                  placeholder="Enter your password"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.button
                variants={itemVariants}
                type="submit"
                disabled={loading}
                className="w-full mt-6 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 text-white font-semibold py-2 px-4 rounded-lg transition-all disabled:opacity-50"
              >
                {loading ? 'Logging in...' : 'Login'}
              </motion.button>
            </motion.form>
          )}

          {/* Register Form */}
          {!isLoginMode && (
            <motion.form
              key="register"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              onSubmit={handleRegister}
              className="space-y-4"
            >
              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  name="fullName"
                  value={registerForm.fullName}
                  onChange={handleRegisterChange}
                  placeholder="Your full name (optional)"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  disabled={loading}
                />
              </motion.div>

              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  value={registerForm.username}
                  onChange={handleRegisterChange}
                  placeholder="Choose a username"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={registerForm.email}
                  onChange={handleRegisterChange}
                  placeholder="Enter your email"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  value={registerForm.password}
                  onChange={handleRegisterChange}
                  placeholder="Minimum 8 characters"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.div variants={itemVariants}>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={registerForm.confirmPassword}
                  onChange={handleRegisterChange}
                  placeholder="Confirm your password"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                  required
                  disabled={loading}
                />
              </motion.div>

              <motion.button
                variants={itemVariants}
                type="submit"
                disabled={loading}
                className="w-full mt-6 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 text-white font-semibold py-2 px-4 rounded-lg transition-all disabled:opacity-50"
              >
                {loading ? 'Creating account...' : 'Sign Up'}
              </motion.button>
            </motion.form>
          )}

          {/* Demo Credentials */}
          <motion.div
            variants={itemVariants}
            className="mt-6 pt-6 border-t border-gray-700"
          >
            <p className="text-gray-400 text-sm mb-3">Demo Credentials:</p>
            <div className="bg-gray-700/50 p-3 rounded-lg text-xs text-gray-300 space-y-1">
              <p>Username: <span className="text-gray-200">demo</span></p>
              <p>Password: <span className="text-gray-200">demo123456</span></p>
            </div>
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.div variants={itemVariants} className="mt-8 text-center">
          <p className="text-gray-400 text-sm">
            Built with React + TypeScript
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};
