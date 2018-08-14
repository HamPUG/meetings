/*
    C version of spirotri example from
    <https://github.com/ldo/qahirah_examples>.
    Build with a command like

        gcc -o spirotri_c spirotri.c -lcairo -lm

*/

#include <stdbool.h>
#include <math.h>
#include <stdio.h>
#include <cairo/cairo.h>

static const double
    deg = M_PI / 180.0,
    circle = 2 * M_PI;

typedef struct
  {
    float r, g, b;
  } colour_t;
typedef struct
  {
    double x, y;
  } vector_t;

static vector_t
    triangle_corners[3];

static void init_triangle_corners(void)
  {
    for (unsigned int a = 0; a < 3; ++a)
      {
        cairo_matrix_t m;
        cairo_matrix_init_rotate(&m, a * circle / 3);
        vector_t v = {.x = 1, .y = 0};
        cairo_matrix_transform_point(&m, &v.x, &v.y);
        triangle_corners[a] = v;
      } /*for*/
  } /*init_triangle_corners*/

static const vector_t
    triangle_step = {.x = 1.5, .y = sqrt(3) / 2},
    flip_adjust = {.x = 0.5, .y = 0};

static const colour_t colours[3] =
    {
        {.r = 0.2, .g = 0.34, .b = 0.4},
        {.r = 0.4, .g = 0.26, .b = 0.2},
        {.r = 0.36, .g = 0.2, .b = 0.4},
    };

static const float
    pix_size = 700,
    figure_size = 150,
    scale_step = 0.87;

static void draw_cell
  (
    cairo_t * ctx,
    float angle,
    const colour_t * colours
  )
  {
    cairo_save(ctx);
      {
        cairo_matrix_t m;
        cairo_matrix_init_rotate(&m, angle);
        cairo_matrix_scale(&m, figure_size, figure_size);
        cairo_transform(ctx, &m);
      }
    cairo_set_line_width(ctx, cairo_get_line_width(ctx) / figure_size);
      /* compensate for scaling of entire coordinate system */
    for (unsigned int step = 0; step < 15; ++step)
      {
        for (unsigned int i = 0; i < 3; ++i)
          {
            cairo_new_path(ctx);
            cairo_move_to(ctx, triangle_corners[(i + 2) % 3].x, triangle_corners[(i + 2) % 3].y);
            cairo_line_to(ctx, triangle_corners[i].x, triangle_corners[i].y);
            cairo_set_source_rgb(ctx, colours[i].r, colours[i].g, colours[i].b);
            cairo_stroke(ctx);
          } /*for*/
          {
            cairo_matrix_t m;
            cairo_matrix_init_rotate(&m, 5 * deg);
            cairo_matrix_scale(&m, scale_step, scale_step);
            cairo_transform(ctx, &m);
          }
        cairo_set_line_width(ctx, cairo_get_line_width(ctx) / scale_step);
      } /*for*/
    cairo_restore(ctx);
  } /*draw_cell*/

int main
  (
    int argc,
    char ** argv
  )
  {
    int status = 0;
    cairo_status_t csts;
    init_triangle_corners();
    cairo_surface_t * const pix = cairo_image_surface_create
      (
        /*format =*/ CAIRO_FORMAT_ARGB32,
        /*width =*/ lrint(pix_size),
        /*height =*/ lrint(pix_size)
      );
    cairo_t * const ctx = cairo_create(pix);
    cairo_translate(ctx, 0.5 * pix_size, 0.5 * pix_size);
    cairo_set_source_rgb(ctx, 1, 1, 1);
    cairo_paint(ctx);
    cairo_set_source_rgb(ctx, 0, 0, 0);
    cairo_set_line_width(ctx, 2);
    for (int row = -3; row < 4; ++row)
      {
        for (int col = -2; col < 2; ++col)
          {
            const int flip = (row ^ col) & 1;
            cairo_save(ctx);
            cairo_translate
              (
                ctx,
                (col * triangle_step.x + flip_adjust.x * flip) * figure_size,
                (row * triangle_step.y + flip_adjust.y * flip) * figure_size
              );
            draw_cell( ctx, flip * 180 * deg, colours);
            cairo_restore(ctx);
          } /*for*/
      } /*for*/
    cairo_surface_flush(pix);
    csts = cairo_surface_write_to_png(pix, "spirotri_c.png");
    if (csts != CAIRO_STATUS_SUCCESS)
      {
        fprintf
          (
            stderr,
            "%s: error %d writing PNG file: %s\n",
            argv[0], csts, cairo_status_to_string(csts)
          );
        status = 3;
      } /*if*/
    return
        status;
  } /*main*/
