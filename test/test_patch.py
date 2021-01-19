import pytest
def test_patch_create_from_buffers():
    patch = pygit2.Patch.create_from(
        BLOB_OLD_CONTENT,
        BLOB_NEW_CONTENT,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH

def test_patch_create_from_blobs(testrepo):
    old_blob = testrepo[BLOB_OLD_SHA]
    new_blob = testrepo[BLOB_NEW_SHA]

    patch = pygit2.Patch.create_from(
        old_blob,
        new_blob,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH2

def test_patch_create_from_blob_buffer(testrepo):
    old_blob = testrepo[BLOB_OLD_SHA]
    patch = pygit2.Patch.create_from(
        old_blob,
        BLOB_NEW_CONTENT,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH

def test_patch_create_from_blob_buffer_add(testrepo):
    patch = pygit2.Patch.create_from(
        None,
        BLOB_NEW_CONTENT,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH_ADDED

def test_patch_create_from_blob_buffer_delete(testrepo):
    old_blob = testrepo[BLOB_OLD_SHA]

    patch = pygit2.Patch.create_from(
        old_blob,
        None,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH_DELETED

def test_patch_create_from_bad_old_type_arg(testrepo):
    with pytest.raises(TypeError):
        pygit2.Patch.create_from(testrepo, BLOB_NEW_CONTENT)

def test_patch_create_from_bad_new_type_arg(testrepo):
    with pytest.raises(TypeError):
        pygit2.Patch.create_from(None, testrepo)

def test_context_lines(testrepo):
    old_blob = testrepo[BLOB_OLD_SHA]
    new_blob = testrepo[BLOB_NEW_SHA]

    patch = pygit2.Patch.create_from(
        old_blob,
        new_blob,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    context_count = len(
        [line for line in patch.text.splitlines() if line.startswith(" ")]
    )

    assert context_count != 0

def test_no_context_lines(testrepo):
    old_blob = testrepo[BLOB_OLD_SHA]
    new_blob = testrepo[BLOB_NEW_SHA]

    patch = pygit2.Patch.create_from(
        old_blob,
        new_blob,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
        context_lines=0,
    )

    context_count = len(
        [line for line in patch.text.splitlines() if line.startswith(" ")]
    )

    assert context_count == 0

def test_patch_create_blob_blobs(testrepo):
    old_blob = testrepo[testrepo.create_blob(BLOB_OLD_CONTENT)]
    new_blob = testrepo[testrepo.create_blob(BLOB_NEW_CONTENT)]

    patch = pygit2.Patch.create_from(
        old_blob,
        new_blob,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH

def test_patch_create_blob_buffer(testrepo):
    blob = testrepo[testrepo.create_blob(BLOB_OLD_CONTENT)]
    patch = pygit2.Patch.create_from(
        blob,
        BLOB_NEW_CONTENT,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH

def test_patch_create_blob_delete(testrepo):
    blob = testrepo[testrepo.create_blob(BLOB_OLD_CONTENT)]
    patch = pygit2.Patch.create_from(
        blob,
        None,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH_DELETED

def test_patch_create_blob_add(testrepo):
    blob = testrepo[testrepo.create_blob(BLOB_NEW_CONTENT)]
    patch = pygit2.Patch.create_from(
        None,
        blob,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    assert patch.text == BLOB_PATCH_ADDED

def test_patch_delete_blob(testrepo):
    blob = testrepo[BLOB_OLD_SHA]
    patch = pygit2.Patch.create_from(
        blob,
        None,
        old_as_path=BLOB_OLD_PATH,
        new_as_path=BLOB_NEW_PATH,
    )

    # Make sure that even after deleting the blob the patch still has the
    # necessary references to generate its patch
    del blob
    assert patch.text == BLOB_PATCH_DELETED

def test_patch_multi_blob(testrepo):
    blob = testrepo[BLOB_OLD_SHA]
    patch = pygit2.Patch.create_from(
        blob,
        None
    )
    patch_text = patch.text

    blob = testrepo[BLOB_OLD_SHA]
    patch2 = pygit2.Patch.create_from(
        blob,
        None
    )
    patch_text2 = patch.text

    assert patch_text == patch_text2
    assert patch_text == patch.text
    assert patch_text2 == patch2.text
    assert patch.text == patch2.text