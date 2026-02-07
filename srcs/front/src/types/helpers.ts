export interface OrientationSelectionType {
    value: string;
    label: string;
}

export interface PicturesDisplying {
    id: string;
    file: File;
    url: string;
}

export interface insertedPictures {
    id: string;
    url: string;
}

export interface dateProposing {
    partner_id: number;
    location: string;
    datetime_str: string;
    description: string;
}

