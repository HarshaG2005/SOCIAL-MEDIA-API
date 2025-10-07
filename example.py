# from fastapi import FastAPI,HTTPException,Depends,status
# from pydantic import BaseModel,Field
# import psycopg
# import time
# import models
# import utils
# from schemas import CreatePost,Post,User,CreateUser
# from databases import engine,SessionLocal
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session
# models.Base.metadata.create_all(bind=engine)


# ###################PSYCOPG_DATABASE___CONNECTION___SETUP#############################################################################################################
# # while True:
# #  try:
  
# #    conn = psycopg.connect("dbname=fastapi user=postgres password=Harsha2005 host=localhost")
# #    cur=conn.cursor(row_factory=psycopg.rows.dict_row)
   
# #    print("Successfully connect to the database!")
# #    break
    

# #  except Exception as e:
# #     print(f"Connecting to db wasnt success :{e}")
# #     time.sleep(1)

# ##############################################################################################################################################
# app=FastAPI()
# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#          db.close()

# ################################CREATE_POST##################################################################################
# @app.post("/posts/",response_model=Post)
# async def create_post(post:CreatePost,db:Session=Depends(get_db)):
#     try:   
#         new_post=models.Post(**post.dict())
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#         return new_post
         
#     #    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
#     #     cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
#     #     new_post = cur.fetchone()
#     #     conn.commit()
#          #return new_post
#     except Exception as e:
#     #   conn.rollback()
#       raise HTTPException(status_code=500, detail=str(e))

# #################################SELECT_ALL#######################################################################################

# @app.get('/posts/',response_model=list[Post])
# async def showall(db:Session=Depends(get_db)):
#     try:
#          posts=db.query(models.Post).all()
#     #    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
#     #     cur.execute("""SELECT * FROM posts""")
#     #     posts = cur.fetchall()
#          return posts
        
#     except Exception as e:
#     #   conn.rollback()
#       raise HTTPException(status_code=500, detail=str(e))

     
# ###################SELECT_BY_ID###########################################################################################################
# @app.get("/posts/{id}",response_model=Post)
# async def select(id:int,db:Session=Depends(get_db)):
#     try:
#         post=db.query(models.Post).filter(models.Post.id==id).first()

#         # with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
#         #     cur.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
#         #     post=cur.fetchone()
#         #     print(post)
#         if post==None:
#            raise HTTPException(status_code=404,detail='post not found')
#         return post 
#     except Exception as e:
#         # conn.rollback()
#         raise HTTPException(status_code=500,detail=str(e))   
# ###################UPDATING_POST###############################################################################################
# @app.put("/posts/{id}" )
# async def update_post(id:int,updated:CreatePost,db:Session=Depends(get_db)):
#   try:
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post=post_query.first()
#     # with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
#     #     cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING*""",(updated.title,updated.content,updated.published,str(id)))
#     #     updated_post=cur.fetchone()
#     #     conn.commit()

#     if post==None:
#         raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!")
#     post_query.update(updated.dict(),synchronize_session=False)
#     db.commit()
#     return {"new":post_query.first()}
#   except Exception as e:
#     # conn.rollback()
#     raise HTTPException(status_code=500,detail=str(e))
# #############################DELETE_POST##############################################################################################
# @app.delete("/posts/{id}")
# async def delete_post(id:int,db:Session=Depends(get_db)):
#   try:
#     post=db.query(models.Post).filter(models.Post.id==id)
#     # with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
#     #     cur.execute("""DELETE FROM posts WHERE id=%s RETURNING*""",(str(id),))
#     #     deleted_post=cur.fetchone()
#     #     conn.commit()
#     if post.first()==None:
#         raise HTTPException(status=404,detail=f"post with id:{id} does not exist!")
#     post.delete(synchronize_session=False) 
#     db.commit()
#     return {"message":f"post with id:{id} got deleted:)"}
#   except Exception as e:
#     conn.rollback()
#     raise HTTPException(status_code=404,detail=str(e))
# #########################################################################################################
# @app.post("/create_user",status_code=status.HTTP_201_CREATED,response_model=User)
# async def create_user(user:CreateUser,db:Session=Depends(get_db)):
#             try:
#                 #hash the password
#                 hashed_password=utils.hash(user.password)
#                 user.password=hashed_password
#                 new_user=models.User(**user.model_dump())
#                 db.add(new_user)
#                 db.commit()
#                 db.refresh(new_user)
#                 return new_user
#             except IntegrityError:
#                     db.rollback()
#                     raise HTTPException(
#                            status_code=status.HTTP_400_BAD_REQUEST,
#                            detail="User with that email already exists."
#                                      )
#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
# ###############################################################################################################
# #@app.get("/users",status_code=status.HTTP_201_CREATED,response_model=list(User))
