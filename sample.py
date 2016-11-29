import graphene as gp
import json
import uuid

# from flask import Flask
# from flask_graphql import GraphQLView
# app = Flask(__name__)

data = {}

class Novel(gp.ObjectType):
    id = gp.ID()
    name = gp.String()
    author = gp.String()
    publish_year = gp.Int()



n1 = Novel(id=1, name='twilight', author="meyer", publish_year = 2005)
n2 = Novel(id=2, name='harrypotter', author="jk", publish_year = 1999)
n3 = Novel(id=3, name='gossip girl', author="unknown", publish_year = 1990)
n4 = Novel(id=4, name='comic', author="any", publish_year = 1900)

data = {n1.id:n1, n2.id:n2, n3.id:n3, n4.id:n4}


class AddNovel(gp.Mutation):
    ok = gp.Boolean(description="success or not")
    newbook = gp.Field(lambda: Novel)

    class Input:
        # id = gp.Int()
        name = gp.String()
        authors = gp.String()
        publish_year = gp.Int()

    def mutate(self, args, context, info):
        new_id = 5 # uuid.uuid4()
        addbook = Novel(id=new_id, name=args.get('name'), author=args.get('authors'), publish_year=args.get('publish_year'))
        return AddNovel(newbook=addbook, ok=True)


class Query(gp.ObjectType):
    book = gp.Field(Novel)
    books = gp.List(Novel)

    def resolve_book(self, args, context, info):
        return data[1]

    def resolve_books(self, args, context, info):
        return [data[x] for x in data]


class Mutation(gp.ObjectType):
    add = AddNovel.Field()


schema = gp.Schema(query=Query, mutation=Mutation)
query = '''
    query novel{
      book{
        id
      },
      books {
        id, name, author, publishYear
      }
    }
'''


mu = '''mutation addnewbook {
  add(authors: "cindy", name: "happy", publishYear: 2017) {
    ok
    newbook {
      id, name
    }
  }
}
'''

#app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
    #test_query()
    result = schema.execute(query)
    addresult = schema.execute(mu)
    print(result.data['book'])
    print(result.data['books'])
    print(addresult.data['add']['newbook'])
    # app.run(debug=True)
