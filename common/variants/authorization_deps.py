# class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
#     def __init__(
#         self,
#         *args,
#         public_routes: list[str],
#         **kwargs,
#     ):
#         super().__init__(*args, **kwargs)
#         self.public_routes = public_routes

#     async def __call__(self, request: Request):
#         path = request.scope.get("path")

#         if (path and path in self.public_routes) or request.method == "OPTIONS":
#             return None

#         return await super().__call__(request)


# oauth2_scheme = CustomOAuth2PasswordBearer(
#     "api/v1/auth/login",
#     public_routes=settings.auth_jwt.ALLOW_ANY_ROUTES,
#     scheme_name="CreateUserSchema",
# )


# async def verify_jwt_access_token(token: str = Depends(oauth2_scheme)):
#     try:
#         if not token:
#             return

#     except JWTTokenHasNotBeenProvidedError as error:
#         logger.error(str(error))
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="'Authorization' header has not been provided or not valid",
#         )
#     except ValidationError as error:
#         str_error = str(error)
#         logger.error(str_error)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str_error)
#     except InvalidSignatureError as error:
#         logger.error(str(error))
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Token is not valid. Token verification failed.",
#         )
#     except DecodeError:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="JWT token is not valid",
#         )
#     except ExpiredSignatureError as error:
#         logger.error(str(error))
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Token has been expired."
#         )
#     except IsNotActiveError as error:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="User  is not active"
#         )
#     except NoResultFound as error:
#         logger.error(str(error))
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Data does not exist"
#         )
#     except IntegrityError as error:
#         logger.error(str(error))
#         if "UniqueViolationError" in str(error.orig):
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Inserted data must be unique",
#             )
#         if "ForeignKeyViolationError" in str(error.orig):
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Row with foreign key you trying to insert does not exist",
#             )
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error",
#         )
#     except InvalidPasswordError as error:
#         str_error = str(error)
#         logger.error(str_error)
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str_error)
#     except UnprocessableEntityError as error:
#         str_error = str(error)
#         logger.error(str_error)
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="Incoming data is not valid",
#         )
