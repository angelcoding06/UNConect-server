export enum TypeLike {
  LIKE = 'Like',
  DISLIKE = 'Dislike',
}

interface Ilike {
  UserId: string;
  PostId: string;
  type: TypeLike;
}

export default Ilike;
