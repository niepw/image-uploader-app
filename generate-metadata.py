from onelogin.saml2.settings import OneLogin_Saml2_Settings


def generate_metadata():
    settings = OneLogin_Saml2_Settings(
        custom_base_path="saml/", sp_validation_only=True
    )
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if len(errors) == 0:
        with open("sp_metadata.xml", "wb") as f:
            f.write(metadata)
        print("Metadata written to sp_metadata.xml")
    else:
        print("Metadata validation errors:", errors)


if __name__ == "__main__":
    generate_metadata()
