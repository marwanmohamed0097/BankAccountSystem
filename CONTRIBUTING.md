# Contributing

## Development Workflow
1. Create a feature branch
2. Implement the change
3. Run backend tests
4. Build the frontend
5. Open a pull request

## Backend Tests
```bash
python -m unittest tests.test_bank -v
```

## Frontend Build
```bash
cd frontend
npm run build
```

## Requirements
- Keep secrets out of Git
- Use environment variables
- Keep tests passing
- Follow the existing project structure
