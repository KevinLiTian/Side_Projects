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
}

export const userQuery = (userId: string) => {
  return `*[_type == "user" && _id == '${userId}']`;
};

export const searchQuery = (searchTerm: string) => {
  return `*[_type == "pin" && title match '${searchTerm}*' || category match '${searchTerm}*' || about match '${searchTerm}*']{
    image {
      asset -> {
        url
      }
    },
    _id,
    destination,
    postedBy -> {
      _id,
      userName,
      image
    },
    save[] {
      _key,
      postedBy -> {
        _id,
        userName,
        image
      },
    },
  }`;
};

export const feedQuery = `*[_type == 'pin'] | order(_createAt desc) {
  image {
    asset -> {
      url
    }
  },
  _id,
  destination,
  postedBy -> {
    _id,
    userName,
    image
  },
  save[] {
    _key,
    postedBy -> {
      _id,
      userName,
      image
    },
  },
}`;

export const fetchUser = (): User => {
  return localStorage.getItem('user') !== 'undefined'
    ? JSON.parse(localStorage.getItem('user')!)
    : localStorage.clear();
};
