import fs from 'fs';
import path from 'path';

// Define log levels
const LOG_LEVELS = {
    INFO: 'INFO',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    DEBUG: 'DEBUG',
};

// Set the log level (can be adjusted based on environment)
const CURRENT_LOG_LEVEL = LOG_LEVELS.DEBUG; // Change to INFO, WARNING, or ERROR as needed

// Log file path
const LOG_FILE_PATH = path.join(__dirname, 'app.log');

/**
 * Logs a message with a specific log level.
 * @param {string} level - The log level (INFO, ERROR, WARNING, DEBUG).
 * @param {string} message - The message to log.
 */
const logMessage = (level, message) => {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}\n`;

    // Log to console
    console.log(logEntry.trim());

    // Log to file
    fs.appendFile(LOG_FILE_PATH, logEntry, (err) => {
        if (err) {
            console.error('Failed to write to log file:', err);
        }
    });
};

/**
 * Logs an informational message.
 * @param {string} message - The message to log.
 */
export const logInfo = (message) => {
    if (CURRENT_LOG_LEVEL === LOG_LEVELS.DEBUG || CURRENT_LOG_LEVEL === LOG_LEVELS.INFO) {
        logMessage(LOG_LEVELS.INFO, message);
    }
};

/**
 * Logs an error message.
 * @param {string} message - The message to log.
 */
export const logError = (message) => {
    logMessage(LOG_LEVELS.ERROR, message);
};

/**
 * Logs a warning message.
 * @param {string} message - The message to log.
 */
export const logWarning = (message) => {
    if (CURRENT_LOG_LEVEL === LOG_LEVELS.DEBUG || CURRENT_LOG_LEVEL === LOG_LEVELS.WARNING) {
        logMessage(LOG_LEVELS.WARNING, message);
    }
};

/**
 * Logs a debug message.
 * @param {string} message - The message to log.
 */
export const logDebug = (message) => {
    if (CURRENT_LOG_LEVEL === LOG_LEVELS.DEBUG) {
        logMessage(LOG_LEVELS.DEBUG, message);
    }
};

/**
 * Clears the log file.
 */
export const clearLogFile = () => {
    fs.writeFile(LOG_FILE_PATH, '', (err) => {
        if (err) {
            console.error('Failed to clear log file:', err);
        } else {
            logInfo('Log file cleared.');
        }
    });
};
