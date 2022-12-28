export interface DecodedResponse {
  name: string;
  picture: string;
  sub: string;
}

export interface User {
  _id: string;
  _type: string;
  userName: string;
  image: string;
}

export interface Pin {
  _id: string;
  title: string;
  about: string;
  destination: string;
  image: {
    asset: {
      url: string;
    };
  };
  postedBy: {
    _id: string;
    image: string;
    userName: string;
  };
  category: string;
  save:
    | [
        {
          _key: string;
          postedBy: {
            _id: string;
            userName: string;
            image: string;
          };
        }
      ]
    | null;
  comments:
    | [
        {
          postedBy: {
            _id: string;
            image: string;
            userName: string;
          };
          comment: string;
        }
      ]
    | null;
}
