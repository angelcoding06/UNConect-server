export enum TypeLike {
  Like = 'LIKE',
  Dislike = 'DISLIKE',
}

interface Ilike {
  UserId: string;
  PostId: string;
  type: TypeLike;
}

export default Ilike;
