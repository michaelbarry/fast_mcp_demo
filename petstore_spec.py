"""
OpenAPI specification for the Pet Store API.
This file defines the API endpoints and schemas for the pet store.
"""

PETSTORE_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Pet Store API",
        "version": "1.0.0",
        "description": "A simple pet store API"
    },
    "paths": {
        "/pets": {
            "get": {
                "operationId": "listPets",
                "summary": "List all pets",
                "responses": {
                    "200": {
                        "description": "A list of pets",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "name": {"type": "string"},
                                            "type": {"type": "string"},
                                            "age": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "createPet",
                "summary": "Create a new pet",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "age": {"type": "integer"}
                                },
                                "required": ["name", "type"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Pet created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "age": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/pets/{petId}": {
            "get": {
                "operationId": "getPet",
                "summary": "Get a pet by ID",
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Pet found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "age": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Pet not found"
                    }
                }
            }
        }
    }
}
