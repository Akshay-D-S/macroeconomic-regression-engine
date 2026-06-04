# Macroeconomic Regression Engine

A distributed regression evaluation engine built with FastAPI, Celery, Redis, and StatsModels for large-scale macroeconomic variable analysis and statistical model selection.

## Overview

The Macroeconomic Regression Engine is designed to automate the evaluation of multiple predictor combinations against a target variable using Ordinary Least Squares (OLS) regression.

The system generates predictor combinations, executes regression analysis, calculates statistical diagnostics, validates models against configurable thresholds, and returns only statistically acceptable models.

The architecture is optimized for long-running analytical workloads using asynchronous task execution and progress tracking.

---

## Key Features

### Regression Evaluation

* Ordinary Least Squares (OLS) regression using StatsModels
* Support for configurable predictor combinations
* Automatic model fitting and validation

### Statistical Diagnostics

The engine calculates:

* R²
* Adjusted R²
* Multiple R
* Predictor P-values
* Variance Inflation Factor (VIF)

### Model Validation

Models are automatically filtered using configurable thresholds:

* Minimum R²
* Minimum Adjusted R²
* Minimum Multiple R
* Maximum P-value
* Maximum VIF

Only statistically valid models are returned.

### Distributed Processing

* FastAPI REST API
* Celery asynchronous task execution
* Redis task state tracking
* Progress monitoring support

---

## Architecture

<img width="720" height="860" alt="image" src="https://github.com/user-attachments/assets/702fc391-9b77-4932-99e6-783af80dcefc" />


---

## API Endpoints

### Submit Regression Job

```http
POST /run
```

Creates a new asynchronous regression task.

### Check Progress

```http
GET /status/{task_id}
```

Returns task status and completion percentage.

### Retrieve Results

```http
GET /result/{task_id}
```

Returns validated regression models once processing is complete.

---

## Project Structure

```text
app/
├── api/
│   └── routes.py
│
├── core/
│   ├── celery_app.py
│   ├── redis.py
│   └── logging.py
│
├── schemas/
│   ├── request.py
│   └── response.py
│
├── services/
│   ├── combination_engine.py
│   ├── regression_engine.py
│   ├── metrics.py
│   ├── pruning.py
│   ├── validator.py
│   └── tasks.py
│
└── main.py
```

---

## Technology Stack

* Python
* FastAPI
* Celery
* Redis
* StatsModels
* Pandas
* NumPy
* Docker
* Docker Compose

---

## Future Enhancements

* Parallel regression worker scaling
* Automated feature selection
* Enhanced pruning strategies
* Model ranking and scoring
* Cloud-native deployment on AWS
* Regression result visualization

---

## Disclaimer

This project is a standalone analytical engine created for educational and research purposes. No client data, proprietary business logic, or confidential information is included.
