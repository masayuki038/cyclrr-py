export class Content {
  id: number;
  user_id: number;
  title: string;
  content: string;
  display: boolean = true;

  constructor(id?: number,
    user_id?: number,
    title?: string,
    content?: string,
    display?: boolean) { }
}
